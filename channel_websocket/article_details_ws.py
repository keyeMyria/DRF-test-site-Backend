import json
from article.models import (Article,
                            )
from comment.serializers import ArticleCommentSerializer
from django.core.exceptions import ObjectDoesNotExist
from like.models import Like
from comment.models import ArticleComment
from channels import Group
from channels.auth import (channel_session_user,
                           channel_and_http_session_user_from_http
                           )
from django.core.cache import cache
from django.db import transaction


def subscribe_handle(group_name, article):
    article_user_list = cache.get(group_name)
    subscription_set = article.subscription_set.all().prefetch_related('user')

    with transaction.atomic():
        for sub in subscription_set:
            if sub.user.username not in article_user_list:
                sub.new_comments += 1
                sub.save()


def like_handle(pk, user):
    comment = ArticleComment.objects.get(pk=pk)
    try:
        like = Like.objects.get(comment=comment, user=user)
        like.delete()
        return {'text': json.dumps({'like': {'grade': False,
                                             'comment_pk': pk,
                                             'liked_user': user.username}}
                                   )}
    except ObjectDoesNotExist:
        Like.objects.create(comment=comment, user=user)
        return {'text': json.dumps({'like': {'grade': True,
                                             'comment_pk': pk,
                                             'liked_user': user.username}}
                                   )}


def comment_handle(content, target, user, article_pk, group_name):
    serializer = ArticleCommentSerializer(data={'text': content,
                                                'user': user.pk,
                                                }
                                          )
    if serializer.is_valid():
        article = Article.objects.get(primary_key=article_pk)
        target_comment = None
        if target is not None:
            target_comment = ArticleComment.objects.get(pk=target)
        serializer.save(answer_target=target_comment, article=article)
        subscribe_handle(group_name, article)
        return {'text': json.dumps({'new_comment': serializer.data})}
    else:
        return {'text': json.dumps({'errors': serializer.errors})}


def comment_edit_handle(edited_comment_id, text):
    try:
        ArticleComment.objects.get(pk=edited_comment_id)
    except ObjectDoesNotExist:
        return


@channel_and_http_session_user_from_http
def ws_article_connect(message, article_pk):
    try:
        Article.objects.get(primary_key=article_pk)
    except ObjectDoesNotExist:
        message.reply_channel.send({"close": True})

    message.reply_channel.send({"accept": True})
    group_name = 'article-{0}'.format(article_pk)

    if cache.get(group_name) is None:
        cache.set(group_name, [])

    if message.user.is_authenticated():
        username = message.user.username
        if cache.get(username) is None:
            cache.set(username, {})
        group_list = cache.get(username)

        if cache.get(username).get(group_name) is None:
            group_list.update({group_name: 1})
            cache.set(username, group_list)
        else:
            changed_value = cache.get(username).get(group_name)
            changed_value += 1
            group_list.update({group_name: changed_value})
            cache.set(username, group_list)

        if username not in cache.get(group_name):
            user_list = cache.get(group_name)
            user_list.append(username)
            cache.set(group_name, user_list)
            Group(group_name).send({'text': json.dumps({'new_user': username})})
    else:
        pass

    Group(group_name).add(message.reply_channel)
    message.reply_channel.send({'text': json.dumps({'user_list': cache.get(group_name)})})


@channel_session_user
def ws_article_receive(message, article_pk):
    group_name = 'article-{0}'.format(article_pk)
    user = message.user
    text_content = json.loads(message.content.get('text'))
    if user.is_authenticated() is False:
        return message.reply_channel.send({'text': 'authorisation_error'})
    try:
        Group(group_name).send(comment_handle(text_content['comment_text'],
                                              text_content.get('target'),
                                              user,
                                              article_pk,
                                              group_name))
    except KeyError:
        try:
            Group(group_name).send(like_handle(text_content['liked_comment_id'], user))
        except KeyError:
            try:
                Group(group_name).send(comment_edit_handle(text_content['edited_comment_id'],
                                                           text_content.get('new_text')))
            except KeyError:
                return


@channel_session_user
def ws_article_disconnect(message, article_pk):
    group_name = "article-{0}".format(article_pk)

    if message.user.is_authenticated():
        username = message.user.username
        if cache.get(username) is None:
            cache.set(username, {})

        connections_value = cache.get(username).get(group_name)
        user_group_list = cache.get(username)
        if connections_value is not None and connections_value <= 1:
            user_group_list.pop(group_name)
            cache.set(username, user_group_list)

            try:
                user_list = cache.get(group_name)
                user_list.remove(username)
                cache.set(group_name, user_list)
            except:
                pass

            Group(group_name).send({'text': json.dumps({'leaver': username})})
        else:
            connections_value -= 1
            user_group_list.update({group_name: connections_value})
            cache.set(username, user_group_list)
    Group(group_name).discard(message.reply_channel)

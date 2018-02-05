from channels import Group
from channels.generic.websockets import WebsocketConsumer
import json
from article.models import (Article, Subscription)
from comment.models import ArticleComment
from like.models import Like
from like.serializers import LikeSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.db import transaction
from comment.serializers import ArticleCommentSerializer


class ArticleWebSocket(WebsocketConsumer):
    http_user_and_session = True

    def _send_to_article_list_group(self, data):
        return Group('article-list').send(data)

    def _send_to_group(self, data):
        return Group('article-{0}'.format(self.kwargs['article_pk'])).send(data)

    def connection_groups(self, **kwargs):
        return ['article-{0}'.format(kwargs['article_pk'])]

    def _handle_subscribe(self, article):
        group_name = 'article-{0}'.format(self.kwargs['article_pk'])
        subscription_list = article.subscription_set.exclude(user__username__in=cache.get(group_name))

        with transaction.atomic():
            for subscription in subscription_list:
                try:
                    subscription.new_comments += 1
                    subscription.save()
                except ObjectDoesNotExist:
                    pass

    def _handle_like(self, data):
        comment_pk = data.get('like').get('comment_id')
        like_bool = data.get('like').get('liked')
        comment = ArticleComment.objects.select_related('likecounter').get(pk=comment_pk)
        likecounter = comment.likecounter
        try:
            like = Like.objects.get(user=self.message.user, like_counter=likecounter)
            if like.like_status == like_bool:
                like.delete()
                likecounter.refresh_from_db()
                return self._send_to_group({'text': json.dumps({'like': {'like_status': None,
                                                                         'comment_pk': comment_pk,
                                                                         'like_counter': {'likes': likecounter.likes,
                                                                                          'dislikes': likecounter.dislikes}}})})
            else:
                serializer = LikeSerializer(like, data={'like_status': like_bool,
                                                        })
        except ObjectDoesNotExist:
            serializer = LikeSerializer(data={'like_status': like_bool,
                                              })
        if serializer.is_valid():
            serializer.save(user=self.message.user, like_counter=likecounter)
            self._send_to_group({'text': json.dumps({'like': serializer.data})})
        else:
            return self.send(text=json.dumps({'popup_message': serializer.errors}))

    def _handle_new_comment(self, new_comment):
        serializer = ArticleCommentSerializer(data={'text': new_comment.get('new_comment').get('comment_text'),
                                                    'user': self.message.user.pk,
                                                    }
                                              )
        if serializer.is_valid():
            article = Article.objects.get(primary_key=self.kwargs['article_pk'])
            target_comment = None
            target = new_comment.get('new_comment').get('target')
            if target is not None:
                target_comment = ArticleComment.objects.get(pk=target)
            serializer.save(answer_target=target_comment, article=article)
            self._handle_subscribe(article)
            data = {'text': json.dumps({'new_comment': serializer.data})}
            self._send_to_group(data)
            return self._send_to_article_list_group(data)
        else:
            return self.send(text=json.dumps({'popup_message': serializer.errors}))

    def _handle_edit_comment(self, pk):
        pass

    def connect(self, message, **kwargs):
        group_name = 'article-{0}'.format(kwargs['article_pk'])

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
                self._send_to_group(({'text': json.dumps({'new_user': username})}))
        else:
            pass
        return super().connect(message)

    def receive(self, text=None, bytes=None, **kwargs):
        content = json.loads(text)
        return getattr(self, '_handle_' + list(content.keys())[0])(content)

    def disconnect(self, message, **kwargs):
        group_name = 'article-{0}'.format(kwargs['article_pk'])
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
        return super().disconnect(message)

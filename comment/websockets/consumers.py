from channels import Group
from channels.generic.websockets import WebsocketConsumer
import json
from article.models import (Article, Subscription)
from comment.models import ArticleComment
from like.models import Like
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.db import transaction
from comment.serializers import ArticleCommentSerializer


class ArticleCommentWebSocket(WebsocketConsumer):
    http_user_and_session = True

    def _send_to_group(self, data):
        return Group('article-{0}'.format(self.kwargs['article_pk'])).send(data)

    def _handle_edit_comment(self, comment):
        pass

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
            data = {'text': json.dumps({'new_comment': serializer.data})}
            self._send_to_group(data)
        else:
            return self.send(text=json.dumps({'popup_message': serializer.errors}))

    def _handle_like(self, content):
        peeled_content = content.get('like')
        placed_like = peeled_content.get('like_bool')
        like_counter = ArticleComment.objects.get(pk=peeled_content.get('comment_pk')).likecounter
        like_status = None
        try:
            existing_like = Like.objects.get(user=self.message.user,
                                             like_counter=like_counter,
                                             like_status=placed_like
                                             )
            existing_like.delete()
            like_counter.refresh_from_db()
        except ObjectDoesNotExist:
            try:
                existing_like = Like.objects.get(user=self.message.user,
                                                 like_counter=like_counter,
                                                 )
                existing_like.like_status = placed_like
                existing_like.save()
                like_counter.refresh_from_db()
            except ObjectDoesNotExist:
                Like.objects.create(user=self.message.user,
                                    like_counter=like_counter,
                                    like_status=placed_like
                                    )
            like_status = placed_like

        data = {'like': {'comment_pk': peeled_content.get('comment_pk'),
                         'likecounter': {'likes': like_counter.likes, 'dislikes': like_counter.dislikes},
                         'like_status': like_status
                         }
                }
        return self._send_to_group({'text': json.dumps(data)})

    def connection_groups(self, **kwargs):
        return ['article-{0}'.format(kwargs['article_pk'])]

    def connect(self, message, **kwargs):
        print('connection established')
        return super().connect(message, **kwargs)

    def disconnect(self, message, **kwargs):
        pass

    def receive(self, text=None, bytes=None, **kwargs):
        content = json.loads(text)
        return getattr(self, '_handle_' + list(content.keys())[0])(content)

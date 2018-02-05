from channels import Group
from channels.generic.websockets import WebsocketConsumer
from comment.serializers import ArticleCommentSidebar
import json


class ArticleListConsumer(WebsocketConsumer):

    def connection_groups(self, **kwargs):
        return ['article-list']

    def connect(self, message, **kwargs):
        print('connected to article-list')
        return super().connect(message, **kwargs)

    def receive(self, text=None, bytes=None, **kwargs):
        content = json.loads(text)
        return Group('article-list').send(content)

from channels import Group
from channels.generic.websockets import WebsocketConsumer
import json


class UserInfo(WebsocketConsumer):
    http_user_and_session = True

    def connection_groups(self, **kwargs):
        return ['user_{0}'.format(kwargs['username'])]

    def connect(self, message, **kwargs):
        if message.user.username != self.kwargs['username']:
            return self.disconnect(message, **kwargs)
        super().connect(message)
        print('connected-user-ws')

    def receive(self, text=None, bytes=None, **kwargs):
        pass


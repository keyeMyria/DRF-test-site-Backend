from channels import Group
from channels.generic.websockets import WebsocketConsumer
from django.core.cache import cache
import json


class UserOnlineWebSocket(WebsocketConsumer):
    http_user_and_session = True

    def _establish_cache_dict(self):
        if not cache.get('online_users'):
            cache.set('online_users', {})
        user_cache = cache.get('online_users')
        return user_cache

    def connection_groups(self, **kwargs):
        return ['online_users']

    def connect(self, message, **kwargs):
        user_cache = self._establish_cache_dict()
        self.send(text=json.dumps({'online_user_list': [x for x in user_cache.keys()]}))
        cached_user = self.message.user.username\

        if cached_user:
            if user_cache.get(cached_user) is None:
                user_cache.update({cached_user: 1})
            else:
                user_cache.update({cached_user: user_cache.get(cached_user) + 1})
            Group('online_users').send({'text': json.dumps({cached_user: True})})

        cache.set('online_users', user_cache)
        return super().connect(message, **kwargs)

    def disconnect(self, message, **kwargs):
        cached_user = self.message.user.username
        user_cache = self._establish_cache_dict()

        if user_cache.get(cached_user):
            if user_cache.get(cached_user) == 1:
                Group('online_users').send({'text': json.dumps({cached_user: False})})
                user_cache.pop(cached_user)
            elif user_cache.get(cached_user) > 1:
                user_cache.update({cached_user: user_cache.get(cached_user) - 1})

        cache.set('online_users', user_cache)
        return super().disconnect(message, **kwargs)

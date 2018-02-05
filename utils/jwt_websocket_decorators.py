from functools import wraps
from channels.handler import AsgiRequest


def jwt_connect(func):

    @wraps(func)
    def inner_func(message, *args, **kwargs):
        request = AsgiRequest(message)
        token = request.GET.get("token", None)
        if token is None:
            message.close_reply_channel()
    return inner_func()

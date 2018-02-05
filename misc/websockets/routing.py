from channels.routing import route
from . import consumers
from channels import route_class


user_online_routing = [
    route_class(consumers.UserOnlineWebSocket),
]

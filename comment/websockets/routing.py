from channels.routing import route
from . import consumers
from channels import route_class


article_details_routing = [
    route_class(consumers.ArticleCommentWebSocket),
]

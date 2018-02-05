from . import consumers
from channels import route_class


article_list_routing = [
    route_class(consumers.ArticleListConsumer),
]

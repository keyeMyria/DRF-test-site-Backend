from channels import include

channel_routing = [
    include('comment.websockets.routing.article_details_routing',
            path=r"^/ws/article/(?P<article_pk>.+)/$"),
    include('user_data_ws.routing.user_data_routing',
            path=r"^/user/(?P<username>.+)/$"),
    include('article.websockets.routing.article_list_routing',
            path=r"^/article-list/$"),
    include('misc.websockets.routing.user_online_routing',
            path=r"^/ws/online-users/$"),
]

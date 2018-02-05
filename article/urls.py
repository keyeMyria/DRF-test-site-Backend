from django.conf.urls import url
from . import views


urlpatterns = [
    url(regex='^api/load-articles-preview/(?P<page>[0-9]+)/$',
        view=views.ArticleListPreview.as_view()
        ),

    url(regex='^api/get-paginated-data/(?P<page>[0-9]+)/$',
        view=views.ArticleListView.as_view()
        ),

    url(regex='^api/load-articles/page/(?P<page>[0-9]+)/order-by/(?P<order>[\w-]+)/$',
        view=views.ArticleListView.as_view()
        ),

    url(regex='^api/load-articles/search=(?P<search>.*)/page/(?P<page>[0-9]+)/order-by/(?P<order>[\w-]+)/$',
        view=views.ArticleListView.as_view()
        ),

    url(regex='^api/load-articles/tag=(?P<tag>.*)/page/(?P<page>[0-9]+)/order-by/(?P<order>[\w-]+)/$',
        view=views.ArticleListView.as_view()
        ),

    url(regex='^api/article/(?P<pk>[\w-]+)/$',
        view=views.ArticleDetailsView.as_view()
        ),
    url(regex='^api/article/(?P<pk>[\w-]+)/subscribe/$',
        view=views.Subscribe.as_view()
        ),

]

from django.conf.urls import url
from . import views

urlpatterns = [
    url(regex='^api/load-comments/(?P<pk>[\w-]+)/(?P<page>[\d]+)/$',
        view=views.ArticleCommentList.as_view()
        ),
    url(regex='^api/edit-comment/(?P<pk>[\d]+)/$',
        view=views.ArticleCommentAPI.as_view()
        ),
    url(regex='^api/load-recent-comments/$',
        view=views.ArticleCommentGlobalRecentComments.as_view()),

]

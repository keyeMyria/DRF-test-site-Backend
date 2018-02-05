from django.conf.urls import url
from . import views

urlpatterns = [
    url(regex='^api/load-tag-list/$',
        view=views.TagList.as_view()),
]

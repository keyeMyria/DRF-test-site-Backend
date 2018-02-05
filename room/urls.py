from django.conf.urls import url
from . import views

urlpatterns = [
    url(regex='^$',
        view=views.index_page),
    url(regex='^api/load-room-list/(?P<page>[\d]+)/(?P<order_field>[\w-]+)/$',
        view=views.RoomListView.as_view())
]

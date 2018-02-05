from django.conf.urls import url
from . import views


urlpatterns = [
    url(regex='^api/get-blacklist/$',
        view=views.GetBlackList.as_view()
        ),

    url(regex='^api/blacklist/(?P<username>[\w]+)/$',
        view=views.BlackListUser.as_view())
]

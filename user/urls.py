from django.conf.urls import url
from . import views

urlpatterns = [
    url(regex='^api/load-user-settings/$',
        view=views.UserSettingsAPI.as_view()),

    url(regex='^api/theme-filter/$',
        view=views.UserSettingsAPI.as_view()),

    url(regex='^api/load-user-info/(?P<username>[\w-]+)/$',
        view=views.UserInfoAPI.as_view()),
]

from django.conf.urls import url
from .views import MainPageCurrentActivity

urlpatterns = [
    url(regex='^api/get-current-activity/$',
        view=MainPageCurrentActivity.as_view())
]
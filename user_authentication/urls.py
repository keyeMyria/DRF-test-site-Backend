from django.conf.urls import url
from . import views


urlpatterns = [
    url('^api/sign-up/$', views.Registration.as_view()),
    url('^api/sign-in/$', views.SignIn.as_view()),
    url('^api/validate/$', views.CheckAuth.as_view()),
    url('^api/logout/$', views.Logout.as_view()),
    url('^api/get-csrf-token/$', views.GenerateCSRFToken.as_view())
]
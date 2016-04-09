from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^post/(?P<identity>[a-zA-Z0-9]{,16})$', views.view_post, name="post"),
]
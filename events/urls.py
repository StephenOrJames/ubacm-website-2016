from django.conf.urls import url
from events import views

urlpatterns = [
    url(r'^$', views.EventsList.as_view(), name="index"),
]
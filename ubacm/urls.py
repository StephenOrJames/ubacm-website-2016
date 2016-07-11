"""ubacm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from main import views as main
from contacts.views import easy_signup, easy_signup_post

urlpatterns = [
    url(r'^$', main.index, name='index'),
    url(r'^contact$', main.contact, name='contact'),
    url(r'^add$', main.add_user, name="add_user"),
    url(r'^add/rest$', main.add_user_rest, name="add_user_request"),
    url(r'^newsletter/(?P<letter_id>[0-9]+)$', main.show_newsletter, name='newsletter'),
    url(r'^unsubscribe/(?P<email>[a-zA-Z0-9]+)$', main.unsubscribe_email, name='unsubscribe'),
    url(r'^meeting$', main.show_meeting, name='meeting'),
    url(r'^meeting/response$', main.add_response, name='add_response'),
    url(r'^orientation$', easy_signup, name="easy_signup"),
    url(r'^orientation/save$', easy_signup_post, name="easy_signup_post"),

    url(r'^blog/', include('blog.urls', namespace="blog")),

    # Admin Pages
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'

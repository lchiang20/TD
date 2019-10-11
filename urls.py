from django.contrib import admin
from django.conf.urls import include, url
from tutorview.views import index, adminview, studentview,login_request
admin.autodiscover()

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^adminview/$', adminview, name='adminview'),
    url(r'^studentview/$', studentview, name='studentview'),
]

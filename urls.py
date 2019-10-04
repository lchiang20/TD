from django.contrib import admin
from django.conf.urls import include, url
from django.contrib.auth.views import login
from tutorview.views import index, adminview, studentview
admin.autodiscover()
print admin
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^adminview/$', adminview, name='adminview'),
    url(r'^studentview/$', studentview, name='studentview'),
]

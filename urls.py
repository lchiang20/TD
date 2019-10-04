from django.contrib import admin
# from django.urls import path, include
from django.conf.urls import include, url
from . import views
admin.autodiscover()
urlpatterns = [
    # url('', include(admin.site.urls)),
    url('', views.welcome, name = 'index.html')
    # url(r'^login/?$', login, {'template_name': 'index.html'}, name='login')
]

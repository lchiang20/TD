from django.contrib import admin
from django.conf.urls import include, url
from tutorview import views
admin.autodiscover()
urlpatterns = [
    # url('', include(admin.site.urls)),
    url('', views.index, name='index'),
    # url('', views.tutorview, name = 'index.html')
]

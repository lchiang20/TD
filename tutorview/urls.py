from django.urls import path
from . import views


urlpatterns = [
    path('', views.tutorview, name = 'studentrpt.html')
]
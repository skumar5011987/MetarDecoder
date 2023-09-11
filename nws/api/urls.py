
from django.urls import path
from . import views

urlpatterns = [
    path('ping', views.NSWPing.as_view(), name='ping'),
    path('info', views.NSWInfo.as_view(), name='info'),
    
]

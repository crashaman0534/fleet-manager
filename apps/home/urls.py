from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('index/', views.index, name='index'),
    path('new_device/', views.new_device, name='new_device'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('device/<pk>/', views.device, name='device'),
    path('device/<pk>/remove', views.remove_device, name='remove_device'),
    path('topic/<pk>/', views.topic, name='topic'),
    path('topic/<pk>/remove', views.remove_topic, name='remove_topic'),
]

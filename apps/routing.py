# routing.py
from django.urls import re_path
from apps.home import consumers

websocket_urlpatterns = [
    re_path(r'ws/mqtt/(?P<ip_address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(?P<port>\d+)/$', consumers.MQTTConsumer.as_asgi()),
]

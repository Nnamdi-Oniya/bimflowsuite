from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from . import consumers  # Task progress consumer

websocket_urlpatterns = [
    re_path(r'ws/task/(?P<task_id>\w+)/$', consumers.TaskProgressConsumer.as_asgi()),
]
"""
ASGI config for bimflow project.
"""
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import bimflow.routing  # Our WebSocket routes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bimflow.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            bimflow.routing.websocket_urlpatterns
        )
    ),
})
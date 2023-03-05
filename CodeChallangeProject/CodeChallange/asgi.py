import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from .channelsmiddleware import TokenAuthMiddleware
from django.core.asgi import get_asgi_application
import socket_app.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CodeChallange.settings")
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": (
            TokenAuthMiddleware(AllowedHostsOriginValidator(URLRouter(socket_app.routing.websocket_urlpatterns)))
        ),
    }
)

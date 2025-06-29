import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
asgi_app = get_asgi_application()

from .middlewares import JWTAuthMiddleware 
import ipcheck.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ipinfo_project.settings")

application = ProtocolTypeRouter({
    "http": asgi_app,  
    "websocket": JWTAuthMiddleware( 
        URLRouter(
            ipcheck.routing.websocket_urlpatterns
        )
    ),
})
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()  # Initialize Django

# Import after setting up Django
from chat.channels_middleware import TokenAuthMiddlewareStack
import chat.routing

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": TokenAuthMiddlewareStack(
       AuthMiddlewareStack( 
            URLRouter(
            chat.routing.websocket_urlpatterns
        ))
    ),
})

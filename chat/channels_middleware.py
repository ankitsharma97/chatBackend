# chat/channels_middleware.py
# chat/channels_middleware.py

from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
import urllib.parse
from account.tokenAuthentication import TokenAuthentication  # Assuming your TokenAuthentication class is in authentication.py

class TokenAuthMiddlewareStack(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()

        auth = TokenAuthentication()
        user = await auth.authenticate_websocket(scope)
        
        scope['user'] = user

        return await super().__call__(scope, receive, send)



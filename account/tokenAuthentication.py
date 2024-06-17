import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import datetime, timedelta
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
import urllib.parse

User = get_user_model()

class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = self.extract_jwt(request)
        if token is None:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except ExpiredSignatureError:
            raise AuthenticationFailed('Token is expired')
        except InvalidTokenError:
            raise AuthenticationFailed('Token is invalid')

        self.verify_token(payload)
        user_id = payload.get('id')
        if user_id is None:
            raise AuthenticationFailed('Token does not contain user_id')

        user = User.objects.get(id=payload['id'])
        return (user, None)

    def verify_token(self, payload):
        if 'exp' not in payload:
            raise AuthenticationFailed('Token has no expiration date')

        expiry = int(payload['exp'])
        curr = int(datetime.now().timestamp())
        if curr > expiry:
            raise AuthenticationFailed('Token is expired')

    def extract_jwt(self, request):
        # Handle HTTP request headers
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer'):
            return auth_header.split(' ')[1]
        return None

    @database_sync_to_async
    def authenticate_websocket(self, scope):
        # Handle WebSocket headers
        query_string = scope.get('query_string', b"").decode("utf-8")
        query_parameters = urllib.parse.parse_qs(query_string)
        token = query_parameters.get('token', [None])[0]

        if token is None:
            return AnonymousUser()
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except ExpiredSignatureError:
            raise AuthenticationFailed('Token is expired')
        except InvalidTokenError:
            raise AuthenticationFailed('Token is invalid')

        self.verify_token(payload)
        user_id = payload.get('id')
        if user_id is None:
            raise AuthenticationFailed('Token does not contain user_id')

        user = User.objects.get(id=payload['id'])
        return user

    @staticmethod
    def generate_jwt(payload):
        exp = datetime.now() + timedelta(days=1)
        payload['exp'] = int(exp.timestamp())
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

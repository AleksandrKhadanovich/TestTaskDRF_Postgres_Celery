import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from users.models import User


# JWT Authentication
class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        authorization_heaader = request.headers.get('Authorization')
        if not authorization_heaader:
            return None
        token = authorization_heaader.split(' ')[1]
        if not token:
            return None
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except Exception:
            msg = 'Not valid token'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'User not found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'User is inactive.'
            raise exceptions.AuthenticationFailed(msg)

        return user, token

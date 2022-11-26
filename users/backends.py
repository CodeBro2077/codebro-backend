import jwt
from rest_framework import authentication
from .models import User
from django.conf import settings
from rest_framework import exceptions


class JWTAuthentication(authentication.BaseAuthentication):
    auth_header_prefix = 'Token'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).decode('utf-8').split()

        if len(auth_header) != 2 or auth_header[0] != self.auth_header_prefix:
            # если заголовок авторизации имеет неправильный формат
            return None

        token = auth_header[1]
        user = self.get_user(token)
        return user, token

    @staticmethod
    def get_user(token):
        try:
            # поиск id пользователя по токену

            user_id = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')['id']

        except Exception as ex:

            error = 'Невозможно декодировать токен'
            raise exceptions.AuthenticationFailed(error)

        try:
            user = User.objects.get(pk=user_id)

        except Exception as ex:

            error = 'пользователь с таким токеном не существует'
            raise exceptions.AuthenticationFailed(error)

        return user

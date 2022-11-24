from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime, timedelta
import jwt
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email:str, password=None):
        if not email:
            raise ValueError('email not found')

        user = self.model(email=self.normalize_email(email.lower()))

        user.set_password(raw_password=password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):

        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email',
                              db_index=True,
                              unique=True,
                              max_length=35)
    username = models.CharField(verbose_name='имя пользователя',
                                db_index=True,
                                unique=True,
                                max_length=30,
                                blank=True,
                                null=True)
    photo = models.ImageField(verbose_name='аватарка',
                              upload_to='',
                              blank=True,
                              null=True)

    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def token(self):
        return self.generate_jwt_token()

    def generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        },
            settings.SECRET_KEY, algorithm='HS256').decode('utf-8')

        return token



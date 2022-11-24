from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser

from .models import User
from .logics.login import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=35)

    password = serializers.CharField(min_length=4,
                                     max_length=25,
                                     write_only=True)

    token = serializers.CharField(read_only=True)

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create_user(email=email,
                                        password=password)

        return user

    class Meta:
        model = User
        fields = ('email', 'password', 'token')


class LoginSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=35)

    password = serializers.CharField(min_length=4,
                                     max_length=25,
                                     write_only=True)

    token = serializers.CharField(read_only=True)

    def validate(self, attrs):

        name = attrs.get('name')

        if name is None:
            raise ValueError('name not found')

        password = attrs.get('password')

        if password is None:
            raise ValueError('password not found')

        user = authenticate(name=name,
                            password=password)

        if user is None:
            return {'error': 'user with this name and password was not found'}

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


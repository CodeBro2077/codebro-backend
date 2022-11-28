from rest_framework import serializers
from .models import User
from .logics.login import authenticate
from .logics.registration import is_username_taken, is_email_taken


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
        password = attrs.get('password')

        if name is not None and password is not None:

            user = authenticate(name=name,
                                password=password)

            if user is not None:
                return {
                    'email': user.email,
                    'username': user.username,
                    'token': user.token
                }
            raise serializers.ValidationError('user with this name and password was not found')

        raise serializers.ValidationError('auth data not found')


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=35)
    username = serializers.CharField(max_length=30,
                                     required=False)
    github_link = serializers.CharField(max_length=100,
                                        required=False)
    job = serializers.CharField(max_length=35,
                                allow_null=True,
                                allow_blank=True)
    photo = serializers.ImageField(required=False)
    stack = serializers.CharField(required=False)
    job_level = serializers.CharField(source='get_job_level_display',
                                      required=False)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        if username is not None and is_username_taken(username):
            raise serializers.ValidationError('username is already taken')

        if email is not None and is_email_taken(email):
            raise serializers.ValidationError('email is already taken')

        return attrs

    class Meta:
        model = User
        fields = ('email',
                  'username',
                  'github_link',
                  'job',
                  'photo',
                  'stack',
                  'job_level', )

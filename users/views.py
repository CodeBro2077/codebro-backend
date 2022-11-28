from drf_yasg import openapi
from rest_framework.decorators import api_view
from .doc import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .logics.registration import is_username_taken, is_email_taken
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema


class UserAPIView(APIView):
    @swagger_auto_schema(**user_create_doc)
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if is_email_taken(email):
                return Response(status=409, data={'error': 'email is already taken'})
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(status=400)


class LoginAPIView(APIView):
    @swagger_auto_schema(**user_login_doc)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(status=200, data=serializer.validated_data)
        return Response(status=400)


class ProfileAPIView(APIView):
    parser_classes = (MultiPartParser, )
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(**get_profile_doc)
    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(status=200, data=serializer.data)

    @swagger_auto_schema(**update_profile_doc)
    def patch(self, request):
        serializer = ProfileSerializer(instance=request.user,
                                       data=request.data,
                                       partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(400)


@swagger_auto_schema(method="get", **is_authenticated_doc)
@api_view()
def is_authenticated_view(request):
    user = request.user
    response = {
        'is_authenticated': user.is_authenticated
    }

    return Response(status=200, data=response)


@swagger_auto_schema(method='get', **is_username_taken_doc)
@api_view()
def is_username_taken_view(request, username):
    response = {
        'is_username_taken': is_username_taken(username)
    }

    return Response(status=200, data=response)


@swagger_auto_schema(method='get', **is_email_taken_doc)
@api_view()
def is_email_taken_view(request, email):
    response = {
        'is_email_taken': is_email_taken(email)
    }

    return Response(status=200, data=response)
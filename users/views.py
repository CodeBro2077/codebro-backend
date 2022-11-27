from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .logics.registration import is_username_taken, is_email_taken
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated


class UserAPIView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = ProfileSerializer(user)

            return Response(status=200, data=serializer.data)

        return Response(status=403)

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
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(status=200, data=serializer.validated_data)
        return Response(status=400)


class ProfileAPIView(APIView):
    parser_classes = (MultiPartParser, JSONParser)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = ProfileSerializer(user)
            return Response(status=200, data=serializer.data)
        return Response(status=403)

    def patch(self, request):
        serializer = ProfileSerializer(instance=request.user,
                                       data=request.data,
                                       partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(400)


@api_view()
def is_authenticated_view(request):
    user = request.user
    response = {
        'is_authenticated': user.is_authenticated
    }

    return Response(status=200, data=response)


@api_view()
def is_username_taken_view(request, username):
    response = {
        'is_username_taken': is_username_taken(username)
    }

    return Response(status=200, data=response)


@api_view()
def is_email_taken_view(request, email):
    response = {
        'is_email_taken': is_email_taken(email)
    }

    return Response(status=200, data=response)
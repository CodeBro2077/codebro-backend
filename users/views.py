from .logics.registration import is_email_taken
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


class UserAPIView(APIView):
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



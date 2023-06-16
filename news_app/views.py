from .serializers import (
    LoginSerializer,
    UserSerializer
)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import mixins, generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import status
from django.conf import settings
import requests


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"Message": "successfully logout"}, status=204)


class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    
class NewsHeadlinesView(APIView):
    def get(self,request):
        params = request.query_params
        country = params.get("country","")
        if not country:
            a=f"?country=in&apiKey={settings.API_KEY}"
            response = requests.get(settings.BASE_URL+f"?country=in&apiKey={settings.API_KEY}")
            if not response.status_code==200:
                return Response({"Message": "Network error"}, status=500)
            return Response({
                "success":True,
                "data": response.json()},
                status=status.HTTP_200_OK)
        response = requests.get(settings.BASE_URL+f"?country={country}&apiKey={settings.API_KEY}")
        if not response.status_code==200:
            return Response({"Message": "Network error"}, status=500)
        return Response({
            "success":True,
            "data": response.json()},
            status=status.HTTP_200_OK)

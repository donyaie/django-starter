from django.shortcuts import render
from .models import CustomUser 
from .serializers import (MyTokenObtainPairSerializer, RegisterSerializer)

from rest_framework.decorators import api_view , permission_classes
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#Register User
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, FollowRelation, Post, Like, Comment, Content
from .serializers import UserSerializer, FollowRelationSerializer, PostSerializer, LikeSerializer, CommentSerializer, ContentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
import os
from rest_framework import status

SALT=os.getenv("SALT")

class UserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serailzer = UserSerializer(data=request.data)
        if serailzer.is_valid():
            serailzer.save()
            return Response(serailzer.data, status=201)
        return Response(serailzer.errors, status=400)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = serializer.validated_data

        response = Response(tokens)
        return response


class LoginView(APIView):
    def post(self, request, format=None):
        username = request.data["username"]
        password = request.data["password"]
        hashed_password = make_password(password=password, salt=SALT)
        user = User.objects.get(username=username)
        if user is None or user.password != hashed_password:
            return Response(
                {
                    "success": False,
                    "message": "Invalid Login Credentials",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                { "success": True, "message": "You are now logged in!" },
                status=status.HTTP_200_OK,
            )


class SignupView(APIView):
    def post(self, request, format=None):
        request.data["password"] = make_password(password=request.data["password"], salt=SALT)
        serailzer = UserSerializer(data=request.data)
        if serailzer.is_valid():
            serailzer.save()
            return Response(serailzer.data, status=201)
        
        return Response(serailzer.errors, status=400)
        
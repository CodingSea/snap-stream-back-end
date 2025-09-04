from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, FollowRelation, Post, Like, Comment
from .serializers import UserSerializer, FollowRelationSerializer, PostSerializer, LikeSerializer, CommentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
import os
from rest_framework import status
from cloudinary.templatetags import cloudinary
from random import randint

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
    

class PostView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def upload_image_cloudinary(self, request, image_name):
        cloudinary.uploader.upload(
            request.FILES['image'],
            public_id=image_name,
            crop='limit',
            width='2000',
            height='2000',
            eager=[
                {'width': 200, 'height': 200,
                  'crop': 'thumb', 'gravity ': 'auto',
                  'radius': 20, 'effect': 'sepia'},
                {'width': 100, 'height': 150,
                 'crop': 'fit', 'format ': 'png'}
            ],
            tags=['image_ad', 'NAPI']
        )
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            try:
                imageName = '{0}_v{1}'.format(request.FILES['file'].name.split('.')[0], randint(0, 100))
                self.upload_image_cloudinary(request, imageName)
                serializer.save(image_ad=imageName)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                return Response({'image': 'Please upload a valid image'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(serializer)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        


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
        
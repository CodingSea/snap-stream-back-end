from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Post, Comment
from .serializers import UserSerializer, PostReadSerializer, PostWriteSerializer, CommentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
import os
from rest_framework import status
import cloudinary
import cloudinary.uploader
from random import randint
from django.db.models import Q

SALT=os.getenv("SALT")

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
        posts = Post.objects.select_related("user").all().order_by('-created_at')
        serializer = PostReadSerializer(posts, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    # This code was mostly taken from the internet but it was changed to fit my model
    def post(self, request):
        file = request.FILES.get('file')
        if file:
            upload_result = cloudinary.uploader.upload(file)
            data = request.data
            data["file"] = upload_result['secure_url']
            data["file_id"] = upload_result["public_id"]
            serializer = PostWriteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'No file provided.'}, status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    def get(self, request, id):
        posts = Post.objects.select_related("user").filter(user = id).order_by('-created_at')
        serializer = PostReadSerializer(posts, many=True)
        return Response(serializer.data, status.HTTP_200_OK) 

class SinglePostView(APIView):
    def get(self, request, id):
        post = Post.objects.get(id=id)
        serializer = PostReadSerializer(post, many=False)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, id):
        Post.objects.get(id=id).delete()
        return Response(status.HTTP_200_OK)
    
    def put(self, request, id):
        post = Post.objects.get(id=id)
        serializer = PostWriteSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    

class SingleUserView(APIView):
    def get(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status.HTTP_200_OK)
    

class LikePostView(APIView):
    def get(self, request, postId, userId):
        post = Post.objects.get(id=postId)
        user = User.objects.get(id=userId)

        if user in post.likes.all():
            post.likes.remove(userId)
        else:
            post.likes.add(userId)
        
        post.save()

        serializer = PostReadSerializer(post, many=False)
        return Response(serializer.data, status.HTTP_200_OK)


class SearchPostsView(APIView):
    def post(self, request):
        search_text = request.data.get("search_text")

        if search_text is None:
            posts = Post.objects.all().order_by('-created_at')
        else:
            posts = Post.objects.filter(Q(caption__icontains=search_text)).order_by('-created_at')
        
        serializer = PostReadSerializer(posts, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    

class FollowView(APIView):
    def post(self, request, userId):
        target_user = User.objects.get(id=userId)
        userId = request.data.get("userId")
        user = User.objects.get(id=userId)

        if target_user in user.followings.all():
            user.followings.remove(target_user.id)
            target_user.followers.remove(user.id)
        else:
            user.followings.add(target_user.id)
            target_user.followers.add(user.id)
        
        user.save()

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status.HTTP_200_OK)


class HomeView(APIView):
    def get(self, request, id):
        user = User.objects.get(id=id)
        posts = Post.objects.all()
        
        print("User followings: ",user.followings)
        
        serializer = PostReadSerializer(posts, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

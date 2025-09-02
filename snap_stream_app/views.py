from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, FollowRelation, Post, Like, Comment, Content
from .serializers import UserSerializer, FollowRelationSerializer, PostSerializer, LikeSerializer, CommentSerializer, ContentSerializer


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
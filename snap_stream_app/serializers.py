from rest_framework import serializers
from .models import User, FollowRelation, Post, Like, Comment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from cloudinary.templatetags import cloudinary

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class FollowRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRelation
        fields = '__all__'
        depth = 1

    
class PostReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        depth = 1

class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        depth = 1


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
        }
        # Add custom user-related data (e.g., vendor info)
        return data
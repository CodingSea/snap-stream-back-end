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

    
class PostSerializer(serializers.ModelSerializer):
    file = serializers.CharField(required=True)
    class Meta:
        model = Post
        fields = '__all__'


    def to_representation(self, instance):
        representation = super(ContentSerializer, self).to_representation(instance)
        imageUrl = cloudinary.utils.cloudinary_url(
            instance.image, width=100, height=150, crop='fill')

        representation['image'] = imageUrl[0]
        return representation


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
        }
        # Add custom user-related data (e.g., vendor info)
        return data
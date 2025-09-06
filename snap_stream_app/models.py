from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.CharField(null=True)
    profile_image_id = models.CharField(null=True)
    
    class RoleOptions(models.TextChoices):
        USER = "user", "User"
        ADMIN = "admin", "Admin"
        
    role = models.CharField(choices=RoleOptions.choices, default=RoleOptions.USER)

    class Meta:
        db_table = 'user'


class FollowRelation(models.Model):
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_user')
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_user')

    class Meta:
        db_table = 'follow_relation'


class Post(models.Model):
    caption = models.CharField(max_length=255)
    file = models.CharField()
    file_id = models.CharField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'like'


class Comment(models.Model):
    content = models.CharField
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comment'
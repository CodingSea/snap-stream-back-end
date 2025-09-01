from django.db import models


class User(models.Model):
    username = models.CharField(max_length=80)
    password = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    profile_image = models.CharField()
    profile_image_id = models.CharField()
    
    class RoleOptions(models.TextChoices):
        USER = "User"
        ADMIN = "Admin"
        
    role = models.CharField(choices=RoleOptions.choices, default=RoleOptions.USER)


class FollowRelation(models.Model):
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, on_delete=models.CASCADE)
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=80)
    password = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    profile_image = models.CharField()
    profile_image_id = models.CharField()
    
    class RoleOptions(models.TextChoices):
        USER = "user", "User"
        ADMIN = "admin", "Admin"
        
    role = models.CharField(choices=RoleOptions.choices, default=RoleOptions.USER)


class FollowRelation(models.Model):
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    caption = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.CharField
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Content(models.Model):
    file = models.CharField()
    order = models.IntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
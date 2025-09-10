from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.CharField(null=True)
    profile_image_id = models.CharField(null=True)

    followings = models.ManyToManyField('self', related_name="following", symmetrical=False, blank=True)
    
    class RoleOptions(models.TextChoices):
        USER = "user", "User"
        ADMIN = "admin", "Admin"
        
    role = models.CharField(choices=RoleOptions.choices, default=RoleOptions.USER)

    class Meta:
        db_table = 'user'


class Post(models.Model):
    caption = models.CharField(max_length=255)
    file = models.CharField()
    file_id = models.CharField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    class Meta:
        db_table = 'post'
    
    def number_of_likes(self):
            return self.likes.count()



class Comment(models.Model):
    content = models.CharField(default="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'
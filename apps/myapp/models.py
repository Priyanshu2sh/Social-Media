from django.db import models
from apps.accounts.models import User

# Create your models here.
class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PostFiles(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    file = models.FileField(upload_to='post_files', null=False, blank=False)

class Follows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_user')
    created_at = models.DateTimeField(auto_now_add=True)

class Likes(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    replied_to = models.ForeignKey('myapp.Comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Saved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
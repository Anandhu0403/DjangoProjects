from django.db import models
from post.models import Post
# Create your models here.
from django.contrib.auth.models import User

class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body= models.TextField()
    date=models.DateTimeField(auto_now_add=True)



from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from post.models import Post
# Create your models here.

def user_directory_path(instance,filename):
    return 'user{0}/{1}'.format(instance.user.id,filename)

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50,null=True,blank=True)
    last_name=models.CharField(max_length=50,null=True,blank=True)
    location=models.CharField(max_length=50,null=True,blank=True)
    url=models.URLField(max_length=1000,null=True,blank=True)
    bio=models.TextField(max_length=150,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    picture=models.ImageField(upload_to=user_directory_path,blank=True,null=True,verbose_name='Picture',default="default.jpg")
    favorite=models.ManyToManyField(Post,blank=True)

    # def __str__(self):
    #     return self.first_name

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    post_save.connect(create_user_profile, sender=User)
    post_save.connect(save_user_profile, sender=User)

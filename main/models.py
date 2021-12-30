import datetime

from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    bio = models.CharField(max_length=350, blank=True)
    profile_pic = models.ImageField(upload_to='ProfilePicture/')
    profile_avatar = models.ImageField(upload_to='AvatarPicture/')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Image(models.Model):
    image = models.ImageField(upload_to ='pictsagram/')
    image_caption = models.CharField(max_length=700)
    tag_someone = models.CharField(max_length=50,blank=True)
    imageuploader_profile = models.ForeignKey(User, on_delete=models.CASCADE,null='True', blank=True)
    image_likes = models.ManyToManyField('Profile', default=False, blank=True, related_name='likes')
    date = models.DateTimeField(auto_now_add=True, null= True)

    def __str__(self):
        return self.image_caption


class Comments (models.Model):
    comment_post = models.CharField(max_length=150)
    author = models.ForeignKey('Profile',related_name='commenter' , on_delete=models.CASCADE)
    commented_image = models.ForeignKey('Image', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author

class UserFollowing(models.Model):
    # user doing the following
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    # user being followed
    followed_user = models.ForeignKey(User, related_name="followed_user", on_delete=models.CASCADE)

    def __str__(self):
        return self.followed_user.username

        # access data with user = User.objects.get(user_id=request.user)
        # user.followed_user.all()
from django.db import models
from allauth.socialaccount.models import SocialAccount

class User(models.Model):
    email = models.CharField(max_length=200, unique=True)
    username = models.CharField(max_length=200, unique=True)
    is_admin = models.BooleanField(default=False)

class Message(models.Model):
    content = models.CharField(max_length=200)
    timestamp = models.DateTimeField(max_length=30,auto_now_add=True)
    room = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    edited_from = models.ForeignKey("self", on_delete=models.CASCADE,blank=True,null=True)

class Room(models.Model):
    name = models.CharField(max_length=200,unique=True)
    is_private = models.BooleanField(default=False)
    author = models.CharField(max_length=200,default='seorregom@gmail.com')
    accepted_users = models.ManyToManyField(User,blank=True)
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follows = models.ManyToManyField("self", symmetrical=False, related_name="followers")


class Posts(models.Model):
    text = models.TextField(max_length=512)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts")
    unlikes = models.ManyToManyField(User, related_name="unliked_posts")

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follows = models.ManyToManyField("self", symmetrical=False, related_name="followers")

    def __str__(self):
        return self.username

    def serializes(self):
        return {
            "id": self.id,
            "followers": self.followers.count(),
            "following": self.follows.count(),
            "username": self.username
        }


class Post(models.Model):
    text = models.TextField(max_length=512)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts")
    unlikes = models.ManyToManyField(User, related_name="unliked_posts")

    def __str__(self):
        return f"{self.owner} post at {self.timestamp}"

    # API to return the post in JSON format
    def serializes(self):
        return {
            "id": self.id,
            "text": self.text,
            "owner": self.owner.serializes(),
            "timestamp": self.timestamp,
            "likes": self.likes.count(),
            "unlikes": self.unlikes.count(),
            "likers": [x.id for x in self.likes.all()]
        }


from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # watchlist = models.ManyToManyField(Listing, blank=True, related_name="watchlist")
    pass


class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024, blank=True)
    min_bid = models.IntegerField(default=0)
    image_url = models.CharField(max_length=512, blank=True)
    current_biggest_bid = models.IntegerField(default=0)
    listing_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", default=1)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    is_closed = models.BooleanField(default=False)

    FASHION = 'FA'
    TOYS = 'TO'
    HOME = 'HO'
    ELECTRONICS = 'EL'
    OTHER = "OT"
    CATEGORIES_CHOICES = [
        (FASHION, "Fashion"),
        (TOYS, "Toys"),
        (HOME, "Home"),
        (ELECTRONICS, "Electronics"),
        (OTHER, "Other")
    ]
    category = models.CharField(
        max_length=2,
        choices=CATEGORIES_CHOICES,
        default=OTHER
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.CharField(max_length=1024)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment_on = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.writer} comment on {self.comment_on}"


class Bid(models.Model):
    amount = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid_on = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.author} bid {self.amount} on {self.bid_on}"

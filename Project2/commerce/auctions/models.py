from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    pass

class Bid(models.Model):
    
    bid = models.IntegerField(default = 0)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "bid")

    def __str__(self):
        return f"User {self.user} bids {self.bid}."


class Auction_Listing(models.Model):
    
    # has user_id as foreign key, if user is deleted so is this auction listing
    # related_name specifies how to fin this data from the user table (in reverse)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name="auction_listings", default = None)

    # ITEM INFORMATION ---
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=50)
    create = models.DateTimeField(auto_now_add=True, blank=True)
    # A user can have many watchlists and a watchlists can have a lot of users watching it
    watchlist = models.ManyToManyField(User, blank=True, related_name="watch_listings")
    
    # BID INFORMATION ---
    bid = models.ForeignKey(Bid, on_delete = models.CASCADE, related_name = "auction_listings", default = None)
    closed = models.BooleanField(default=False, blank=True, null=True)
    url = models.CharField(max_length=1000)
    
    def __str__(self): 
        return f"Item: {self.name} - Bid: {self.bid}."


class Comment(models.Model):
    
    create = models.DateTimeField(auto_now_add=True, blank=True)
    text = models.CharField(max_length=500)
    # writer needs to have a user
    writer = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comments")
    # has auction_listing_id as foreign key
    listing = models.ForeignKey(Auction_Listing, on_delete = models.CASCADE, related_name = "comments")

    def __str__(self):
        return f"{self.writer} wrote the following comment for listing {self.listing} on {self.create}: {self.text}"
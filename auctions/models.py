from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    
    name = models.CharField (max_length= 50, unique= True)

    def __str__ (self):
        return self.name

class AuctionListing(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length= 64)
    description = models.CharField (max_length= 256)
    starting_bid = models.DecimalField (max_digits= 5, decimal_places= 2)
    image = models.CharField(blank= True, null= True, max_length= 500)
    categories = models.ManyToManyField(Category, blank= True, null=True)
    closed = models.BooleanField(default= False)

    def __str__(self):
        return f"{self.user} - {self.title}"

class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="auction_bids")
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.bid_amount}"

class Comment(models.Model):
    comment = models.CharField (max_length= 128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="auction_comments")
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment}"
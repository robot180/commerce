from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inventory")
    list_item = models.CharField(max_length=60)
    description = models.TextField(max_length=500, blank="True")
    current_bid = models.DecimalField(decimal_places=2, max_digits=20, null="False")
    categoryType= models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="listings", null='True', blank='True')
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/', default="/images/No-Image-Placeholder.svg.png", blank=True, null='False')
    highest_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", null='True', blank='True')

    def __str__(self):
        return f"{self.id}: {self.list_item} seller: {self.seller}. Current bid = {self.current_bid}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watched")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchers")

    def __str__(self):
        return f"{self.listing}"
        #note even though the watchlists model stores just a fk for listing, it can return the actual listing as well as the def __str__
        #it's basically an entire listing instance stored in the watchlist table as a foreign key


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alluserComments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="allComments")
    comment = models.CharField(max_length=250, blank="False", null='False')

    def __str__(self):
        return f"{self.user}: {self.comment}"


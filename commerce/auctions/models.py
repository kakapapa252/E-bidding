from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings


class User(AbstractUser):
    pass

class CategoryList(models.Model):
    category = models.TextField()

    def __str__(self):
        return (f"Category {self.category}")

class Listing(models.Model):
    idx = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    summary = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    listing_date = models.DateTimeField("date_listed", default=timezone.now())
    thumbnail = models.ImageField(null=True, blank=True,)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,)
    category = models.ForeignKey(CategoryList, on_delete=models.CASCADE)

    def __str__(self):
        return (f"This product {self.title} has id: {self.idx}")


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(Listing,on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=timezone.now())
    slug = models.CharField(max_length=30, null=True, blank=True,)

    def __str__(self):
        return (f"This product {self.item.title} has id: {self.item.idx} added by {self.user}")

class BiddingList(models.Model):
    bid = models.DecimalField(max_digits=10,decimal_places=2,)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(Listing,on_delete=models.CASCADE)
    
    added_date = models.DateTimeField(default=timezone.now())


class CommentList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(Listing,on_delete=models.CASCADE)
    comment = models.TextField()
    added_date = models.DateTimeField(default=timezone.now())
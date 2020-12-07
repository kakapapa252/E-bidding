from django.contrib import admin
from .models import *

from django.db import models
# Register your models here.

class UserAdmin(admin.ModelAdmin):
	fields = ['username', 'email', 'password',]

admin.site.register(User, UserAdmin)
		
admin.site.register(CategoryList)

admin.site.register(Listing)

admin.site.register(Wishlist)

admin.site.register(BiddingList)

admin.site.register(CommentList)

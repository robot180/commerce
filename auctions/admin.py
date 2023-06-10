from django.contrib import admin

from .models import *

def getFieldsModel(model):
    return [field.name for field in model._meta.get_fields()]

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "seller", "list_item", "description", "current_bid", 'categoryType', 'active', 'image', 'highest_bidder',)

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = getFieldsModel(Watchlist)

admin.site.register(Listing, ListingAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
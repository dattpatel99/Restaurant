from django.contrib import admin
from restaurant.models import Item, CartItem

# Register your models here.
admin.site.register(Item)
admin.site.register(CartItem)
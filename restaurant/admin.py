from django.contrib import admin
from restaurant.models import Item, SignUp, CartItem

# Register your models here.
admin.site.register(Item)
admin.site.register(SignUp)
admin.site.register(CartItem)
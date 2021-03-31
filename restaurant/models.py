from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone


# Create your models here.
class Item(models.Model):
    itemName =  models.CharField(max_length=30)
    image = models.ImageField(default='default.png', upload_to='images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length =30, default="Food")
    

    def __str__(self):
        return self.itemName

class SignUp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    phoneNum = models.CharField(max_length=10,null=True)
    address = models.TextField()

class CartItem(models.Model):
    orderId = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items_list = models.CharField(max_length=5000) #Try with TextField too
    order_date = models.DateField(auto_now_add=True, null=True, blank=True)
from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone


# Create your models here.
class Items(models.Model):
    itemName =  models.CharField(max_length=30)
    image = models.ImageField(default='default.png', upload_to='images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.itemName

class SignUp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    phoneNum = models.CharField(max_length=10,null=True)
    address = models.TextField()

class CartItems():
    ORDER_STATUS = (
        ('Active', 'Active'),
        ('Delivered', 'Delivered')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items_list = models.TextField()
    order_date = models.DateField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Active')
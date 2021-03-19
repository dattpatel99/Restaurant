from django.db import models
from django.contrib.auth.models import User 


# Create your models here.
class Items(models.Model):
    itemName =  models.CharField(max_length=30)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.itemName

class SignUp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    phoneNum = models.CharField(max_length=10,null=True)
    address = models.TextField()
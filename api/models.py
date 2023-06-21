from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255,blank=True, null=True)
    phone_number = models.CharField(max_length=15,blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user_id = models.OneToOneField(UserProfile,related_name='user_cart', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='product_cart')

    def __str__(self):
        return self.user_id.user.username
    
# class Order(models.Model):
#     cart = models.ForeignKey(Cart, related_name='order_cart', on_delete=models.CASCADE)
    
""" API App Model. """
from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    """ a Profile model  """
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["price"]


class Cart(models.Model):
    user_id = models.OneToOneField(
        Profile, related_name="user_cart", on_delete=models.PROTECT
    )
    products = models.ManyToManyField(Product, related_name="product_cart")

    def __str__(self):
        return self.user_id.user.username

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class Order(models.Model):
    user = models.ForeignKey(
        Profile, related_name="user_order", on_delete=models.PROTECT
    )
    products = models.ManyToManyField(
        Product, related_name="product_order", null=True, blank=True
    )
    def __str__(self):
        return self.user.user.username

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

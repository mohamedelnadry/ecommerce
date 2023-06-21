""" API App Model. """

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    """
    Profile model that extends the User model with additional fields.
    Fields: address, phone_number.
    """

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        """Returns the username of the user."""
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class Product(models.Model):
    """
    Product model with fields name and price.
    """

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        """Returns the name of the product."""
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["price"]


class Cart(models.Model):
    """
    Cart model with a OneToOne relationship with Profile and ManyToMany relationship with Product.
    """

    user_id = models.OneToOneField(
        Profile, related_name="user_cart", on_delete=models.PROTECT
    )
    products = models.ManyToManyField(Product, related_name="product_cart")

    def __str__(self):
        """Returns the username of the user who owns the cart."""
        return self.user_id.user.username

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class Order(models.Model):
    """
    Order model with a ForeignKey relationship with Profile and ManyToMany relationship with Product.
    """

    user = models.ForeignKey(
        Profile, related_name="user_order", on_delete=models.PROTECT
    )
    products = models.ManyToManyField(
        Product, related_name="product_order", null=True, blank=True
    )

    def __str__(self):
        """Returns the username of the user who placed the order."""
        return self.user.user.username

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

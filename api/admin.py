""" API:admin file """
from django.contrib import admin

from .models import Product, Cart, Order


class ProductAdmin(admin.ModelAdmin):
    """Admin interface for the Product model."""
    list_display = ('name', 'price')
    search_fields = ['name']


admin.site.register(Product, ProductAdmin)


class CartAdmin(admin.ModelAdmin):
    """Admin interface for the Cart model."""
    list_display = ('user_id',)
    search_fields = ['user_id__user__username']


admin.site.register(Cart, CartAdmin)


class OrderAdmin(admin.ModelAdmin):
    """Admin interface for the Order model."""
    list_display = ('user',)
    search_fields = ['user__user__username']


admin.site.register(Order, OrderAdmin)

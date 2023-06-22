""" API:serializer file. """
import re
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Product, Cart, Order


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Includes extra fields for the user's address and phone number.
    """

    address = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "address", "phone_number"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        """
        Validates that the provided email address is valid.
        """
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            raise serializers.ValidationError("Enter a valid email address")
        return value

    def validate_password(self, value):
        """
        Validates that the provided password is at least 8 characters long
        and contains a mix of letters, numbers, and special characters.
        """
        if not re.match(r"^[A-Za-z0-9@#$%^&+=]{8,}$", value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters long and contain letters, numbers, and special characters"
            )
        return value

    def create(self, validated_data):
        """
        Creates a new user and associated profile with the validated data.
        """
        address = validated_data.pop("address")
        phone_number = validated_data.pop("phone_number")
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, address=address, phone_number=phone_number)
        return user


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """

    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model.
    """

    class Meta:
        model = Cart
        fields = ["id", "products"]
        depth = 1


class CreateCartSerializer(serializers.Serializer):
    """
    Serializer for creating and updating a cart.
    """

    product = serializers.IntegerField(required=True)

    def validate_product(self, value):
        """
        Validates that the provided product ID corresponds to a real product.
        """
        product = Product.objects.filter(pk=value)
        if product.exists():
            return product.first()
        raise serializers.ValidationError("Product Not Found")

    def create(self, validated_data):
        """
        Creates a new cart or updates an existing one with the validated data.
        """
        user = self.context["user"]
        product = validated_data.pop("product")
        cart, created = Cart.objects.get_or_create(user_id=user)
        cart.products.add(product)
        return cart


class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model for list views.
    """

    class Meta:
        model = Order
        fields = ["id", "products"]
        depth = 1


class OrderSerializer(serializers.Serializer):
    """
    Serializer for creating orders.
    """

    def create(self, validated_data):
        """
        Creates a new order with the products from the user's cart.
        """
        user = self.context["user"]
        cart = Cart.objects.get(user_id=user)
        order = Order.objects.create(user=user)
        products = cart.products.all()
        if not products:
            raise serializers.ValidationError("No Products in Cart")
        order.products.add(*products)
        cart.products.clear()
        return order

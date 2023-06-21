from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Profile, Product, Cart, Order
from django.contrib.auth.models import User
import re



class ResgisterSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "address", "phone_number"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            raise serializers.ValidationError("Enter a valid email address")
        return value

    def validate_password(self, value):
        if not re.match(r"^[A-Za-z0-9@#$%^&+=]{8,}$", value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters long and contain letters, numbers, and special characters"
            )
        return value

    def create(self, validated_data):
        address = validated_data.pop("address")
        phone_number = validated_data.pop("phone_number")
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(
            user=user, address=address, phone_number=phone_number
        )
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id',"products"]
        depth = 1




class CreateCartSerializer(serializers.Serializer):
    product = serializers.IntegerField(required=True)

    def validate_product(self, value):
        product = Product.objects.filter(pk=value)
        if product.exists():
            return product.first()
        raise serializers.ValidationError("Proudcut Not Found")

    def create(self, validated_data):
        user = self.context["user"]
        product = validated_data.pop("product")
        cart, created = Cart.objects.get_or_create(user_id=user)
        cart.products.add(product)
        return cart

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id',"products"]
        depth = 1



class OrderSerializer(serializers.Serializer):

    def create(self, validated_data):
        user = self.context["user"]
        cart = Cart.objects.get(user_id=user)
        order = Order.objects.create(user=user)
        products = cart.products.all()
        if not products:
            raise serializers.ValidationError("No Products in Card")
        order.products.add(*products)
        cart.products.clear()
        return order




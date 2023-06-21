from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserProfile, Product, Cart
from django.contrib.auth.models import User
import re


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


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
        password = validated_data.pop("password", None)
        address = validated_data.pop("address")
        phone_number = validated_data.pop("phone_number")
        user = User.objects.create_user(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        UserProfile.objects.create(
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
        fields = ["products"]
        depth = 1


class CreateCartSerializer(serializers.Serializer):
    product = serializers.IntegerField(required=True)

    def validate_product(self, value):
        product = Product.objects.filter(pk=value)
        print(product)
        if product.exists():
            return product.first()
        raise serializers.ValidationError("Proudcut Not Found")

    def create(self, validated_data):
        user = self.context["user"]
        product = validated_data.pop("product")
        print(product)
        cart, created = Cart.objects.get_or_create(user_id=user)
        cart.products.add(product)
        return cart

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializer import (
    ResgisterSerializer,
    CartSerializer,
    ProductSerializer,
    CreateCartSerializer,
    CartSerializer,
    OrderSerializer,
    OrderListSerializer
)
from .models import Product, Cart, Order

# Create your views here.


class RegisterVeiw(APIView):
    """Register APi View."""

    permission_classes = [AllowAny]

    def post(self, request):
        """API POST HTTP method."""

        serializer = ResgisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(
            {
                "message": "User registered successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class ProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        queryset = Product.objects.all().order_by("price")
        name = self.request.query_params.get("name", None)
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @property
    def user_cart(self):
        cart, _ = Cart.objects.get_or_create(user_id=self.request.user.profile)
        return cart

    def post(self, request):
        serializer = CreateCartSerializer(
            data=request.data, context={"user": request.user.profile}
        )
        if serializer.is_valid():
            cart = serializer.save()
            return Response(
                {
                    "user": request.user.profile.id,
                    "products": cart.products.values_list("id", flat=True),
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response(
            data=CartSerializer(instance=self.user_cart).data, status=status.HTTP_200_OK
        )

    def delete(self, request):
        serializer = CreateCartSerializer(
            data=request.data, context={"user": request.user.profile}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        product = serializer.validated_data["product"]
        if not self.user_cart.products.filter(id=product.pk).exists():
            return Response(
                {"Errors": "This product doesn't exist in this cart"},
                status=status.HTTP_404_NOT_FOUND,
            )
        self.user_cart.products.remove(product)
        return Response(
            {"Status": "This product removed successfully"}, status=status.HTTP_200_OK
        )


class OrderVeiw(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = OrderSerializer(data = request.data,context={"user": request.user.profile})
        if serializer.is_valid():
            order = serializer.save()
            return Response(
                {"Status": "Order Complete successfully", "order_id": order.id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            order = Order.objects.get(id = kwargs['id'])
            serializer = OrderListSerializer(instance = order)
        else:
            order_list = Order.objects.filter(user=self.request.user.profile)
            serializer = OrderListSerializer(instance=order_list, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )


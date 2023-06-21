from rest_framework import generics, status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Cart, Order, Product
from .serializers import (
    CartSerializer,
    CreateCartSerializer,
    OrderListSerializer,
    OrderSerializer,
    ProductSerializer,
    RegisterSerializer,
)


class RegisterView(views.APIView):
    """
    API view for user registration.

    Accepts POST requests and allows any user (authenticated or not).
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Creates a new user upon receiving a valid POST request.

        Returns a response with HTTP 201 status on success, otherwise HTTP 400.
        """
        serializer = RegisterSerializer(data=request.data)
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
    """
    API view for retrieving product list.

    Uses JWT for authentication.
    """

    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        """
        Returns a queryset of all Products.

        If a 'name' query parameter is present, filters by name.
        """
        queryset = Product.objects.all().order_by("price")
        name = self.request.query_params.get("name", None)
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class CartView(views.APIView):
    """
    API view for cart manipulation.

    Only allows authenticated users and uses JWT for authentication.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @property
    def user_cart(self):
        """
        Returns the user's cart, creating one if it doesn't exist.
        """
        cart, _ = Cart.objects.get_or_create(user_id=self.request.user.profile)
        return cart

    def post(self, request):
        """
        Adds a product to the user's cart upon receiving a valid POST request.

        Returns a response with the updated cart.
        """
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
        """
        Returns the user's current cart.
        """
        return Response(
            data=CartSerializer(instance=self.user_cart).data, status=status.HTTP_200_OK
        )

    def delete(self, request):
        """
        Removes a product from the user's cart upon receiving a valid DELETE request.

        Returns a response indicating the operation's success or failure.
        """
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


class OrderView(views.APIView):
    """
    API view for order manipulation.

    Only allows authenticated users and uses JWT for authentication.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        """
        Creates a new order upon receiving a valid POST request.

        Returns a response with the new order ID.
        """
        serializer = OrderSerializer(
            data=request.data, context={"user": request.user.profile}
        )
        if serializer.is_valid():
            order = serializer.save()
            return Response(
                {"Status": "Order Complete successfully", "order_id": order.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """
        Returns a specific order if an ID is provided, otherwise all the user's orders.
        """
        if "id" in kwargs:
            order = Order.objects.get(id=kwargs["id"])
            serializer = OrderListSerializer(instance=order)
        else:
            order_list = Order.objects.filter(user=self.request.user.profile)
            serializer = OrderListSerializer(instance=order_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializer import (
    ResgisterSerializer,
    UserSerializer,
    CartSerializer,
    ProductSerializer,
    CreateCartSerializer,
    CartSerializer,
    MyTokenObtainPairSerializer,
)
from .models import Product, Cart

# Create your views here.


class RegisterVeiw(APIView):
    def post(self, request):
        serializer = ResgisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserSerializer(user)
            return Response(
                {
                    "user": user_serializer.data,
                    "message": "User registered successfully",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("price")
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class CreateCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateCartSerializer(
            data=request.data, context={"user": request.user.userprofile}
        )
        if serializer.is_valid():
            cart = serializer.save()

            return Response(
                {
                    "user_id": request.user.userprofile.id,
                    "products": cart.products.values_list("id", flat=True),
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartVeiw(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        queryset = Cart.objects.filter(user_id=self.request.user.userprofile)

        return queryset

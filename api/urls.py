from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (
    RegisterView,
    ProductsView,
    CartView,
    OrderView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="API ecommerce",
        default_version="v1",
        description="An Ecommerce API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # User registration endpoint
    path("v1/register", RegisterView.as_view(), name="register"),
    # Products list endpoint
    path("v1/products", ProductsView.as_view(), name="list_products"),
    # User cart endpoint
    path("v1/cart", CartView.as_view(), name="cart"),
    # Create order endpoint
    path("v1/order", OrderView.as_view(), name="order_cart"),
    # Order detail endpoint
    path("v1/order/<int:id>/", OrderView.as_view(), name="order-detail"),
    # Login endpoint
    path("v1/login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Token refresh endpoint
    path("v1/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

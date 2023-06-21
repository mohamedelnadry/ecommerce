from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterVeiw, ProductsView, CartView,OrderVeiw
urlpatterns = [
    path('v1/register',RegisterVeiw.as_view() ,name='register'),
    path('v1/products',ProductsView.as_view(),name='list_products'),
    path('v1/cart',CartView.as_view(),name='cart'),
    path('v1/order',OrderVeiw.as_view(),name='order_cart'),
    path('v1/order/<int:id>/', OrderVeiw.as_view(), name='order-detail'),
    path('v1/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

]

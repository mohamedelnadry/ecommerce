from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterVeiw, LoginView, ProductsView, CreateCartView, CartVeiw
urlpatterns = [
    path('v1/register',RegisterVeiw.as_view() ,name='register'),
    path('v1/login', LoginView.as_view(), name='login'),
    path('v1/products',ProductsView.as_view(),name='list_products'),
    path('v1/cart',CreateCartView.as_view(),name='add_to_cart'),
    path('v1/mycart',CartVeiw.as_view(),name='CartView'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

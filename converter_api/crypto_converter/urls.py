from django.contrib import admin
from django.urls import path
from api.views import ConversionCryptoView, ConversionCoinView, RegisterUserView, ConversionListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

# Endpoints
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/conversion/crypto/", ConversionCryptoView.as_view(), name="conversion_crypto"),
    path("api/conversion/coin/", ConversionCoinView.as_view(), name="conversion_coin"),
    path("api/conversion/", ConversionListView.as_view(), name='conversion_list'),
    path("register/", RegisterUserView.as_view(), name='register_user'),
    path("login/token/", TokenObtainPairView.as_view(), name='token_access'),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token")
]

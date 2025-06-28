from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from accounts.views import EmailTokenObtainPairView, RegisterUserView
from api.views import ConversionCryptoView, ConversionCoinView, ConversionListView, ConversionDeleteView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/conversion/crypto/", ConversionCryptoView.as_view(), name="conversion_crypto"),
    path("api/conversion/coin/", ConversionCoinView.as_view(), name="conversion_coin"),
    path("api/conversion/", ConversionListView.as_view(), name='conversion_list'),
    path("api/conversion/<int:id>", ConversionDeleteView.as_view(), name='conversion_delete'),
    path("register/", RegisterUserView.as_view(), name='register_user'),
    path("login/token/", EmailTokenObtainPairView.as_view(), name='token_access'),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path('token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
]

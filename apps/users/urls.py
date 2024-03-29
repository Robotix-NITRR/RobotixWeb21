from django.urls import path, include
from .views import RegisterView, LogoutAPIView, VerifyEmail,  LoginAPIView, PasswordTokenCheckAPI, RequestPasswordResetEmail, UserViewSet
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework import routers
router = routers.DefaultRouter()
router.register('', UserViewSet)
app_name = "users"

urlpatterns = [
    path('profile/', include(router.urls)),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
]
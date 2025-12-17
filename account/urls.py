# accounts/urls.py
from django.urls import path
from .views import RequestOTPAPIView, VerifyOTPAPIView

urlpatterns = [
    path('request-otp/', RequestOTPAPIView.as_view()),
    path('verify-otp/', VerifyOTPAPIView.as_view()),
]

from django.urls import path
from .views import RegisterView, TOTPVerification

urlpatterns = [
    path('user/register/', RegisterView.as_view(), name='user-register'),
    path('user/otpregister/', TOTPVerification.as_view(), name='otp-register')
]
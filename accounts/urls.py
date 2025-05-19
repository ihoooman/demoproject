from django.urls import path
from .views import (
    SignUpView,
    LoginView,
    LogoutView,
    VerifyOTPView,
    PhoneSignupView,
    SendOTPView
)

app_name = 'accounts'


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('phone-signup/', PhoneSignupView.as_view(), name='phone_signup'),
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
]
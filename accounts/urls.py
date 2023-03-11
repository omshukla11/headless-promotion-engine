from django.urls import path
from .views import index,facebookindex, SignUp, Login, VerifyEmail, LogoutAPIView, RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPIView,GoogleAuth,FacebookAuth,AdminAPI
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('googletemp/',index, name = "index.html"),
    path('facebooktemp/',facebookindex, name = "facebook.html"),
    path('signup/', SignUp.as_view(), name='Signup'),
    path('email-verify/', VerifyEmail.as_view(), name="EmailVerification"),
    path('login/', Login.as_view(), name="Login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('token-refresh/',TokenRefreshView.as_view(),name="RefreshToken"),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name = "password-reset-confirm"),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),name='password-reset-complete'),
    
    path('adminprofile/', AdminAPI.as_view(), name="admin-creation"),

    path('google/',GoogleAuth.as_view(), name = "googleAuth"),
    path('facebook/',FacebookAuth.as_view(), name = "facebookAuth"),
]
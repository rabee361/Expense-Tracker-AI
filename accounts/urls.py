from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view()),
    path('auth/sign-up/',SignUpView.as_view()),
    path('auth/log-in/', LoginView.as_view()),
    path('auth/log-out/', LogoutView.as_view()),
    path('auth/get-code/', GetOTPCodeView.as_view()),
    path('auth/verify-account/<str:pk>/', VerifyAccountView.as_view()),
    path('auth/verify-otp/<str:pk>/', VerifyOTPView.as_view()),
    path('auth/reset-password/<str:pk>/', ResetPasswordView.as_view()),

    path('setting/profile-info/<str:pk>/', ListUserInformationView.as_view()),
    path('setting/update-image/<str:pk>/',UpdateImageUserView.as_view()),

    path('create-account/' , UserAccount.as_view()),
    path('delete-account/<str:pk>' , DeleteAccount.as_view()),
    path('accounts/' , UserAccount.as_view()),


]
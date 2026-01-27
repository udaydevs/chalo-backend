"""Urls are defined here for authentication purposes"""

from django.urls import path

from apps.users.api.views import (
    Login,
    OTPVerification,
    PasswordReset,
    PasswordResetRequest,
    Registration,
    UserDetails,
    GitHubRegistration
)

urlpatterns = [
    path('register/', Registration.as_view()),
    path('login/',  Login.as_view()),
    path('user-info/', UserDetails.as_view()),
    path("github/callback/", GitHubRegistration.as_view()),
    # path("google/callback/", GoogleRegistration.as_view()),
    path('password-reset/request/', PasswordResetRequest.as_view()),
    path('password-reset/verify-otp/', OTPVerification.as_view()),
    path('password-reset/change-password/', PasswordReset.as_view())
]

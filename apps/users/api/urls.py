"""Urls are defined here for authentication purposes"""

from django.urls import path

from apps.users.api.views import (
    GoogleRegistration,
    Login,
    Registration,
    UserDetails,
    GitHubRegistration
)

urlpatterns = [
    path('register/', Registration.as_view()),
    path('login/',  Login.as_view()),
    path('user-info/', UserDetails.as_view()),
    path("github/callback/", GitHubRegistration.as_view()),
    path("google/callback/", GoogleRegistration.as_view()),
]

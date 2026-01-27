"""
URL configuration for CHALO project.
"""
from django.contrib import admin
from django.urls import include, path
from apps.users.api.views import GitHubLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.users.api.urls')),
    path('parties/', include('apps.party.api.urls')),
    path('accounts/', include('allauth.urls')),
    path("dj-rest-auth/social/login/github/", GitHubLogin.as_view()),
    # path("dj-rest-auth/social/login/google/", GoogleLogin.as_view()),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
]

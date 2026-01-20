"""Rewriting authenticate function to retrieve the user details"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class CookieJWTAuthenticaton(JWTAuthentication):
    """
    Docstring for CookieJWTAuthenticaton
    """
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return None

        try:
            validated_token = self.get_validated_token(token)
        except AuthenticationFailed as error:
            return AuthenticationFailed(f"Token validation failed : {error}")

        try:
            user = self.get_user(token)
            return user, validated_token
        except AuthenticationFailed as error:
            return AuthenticationFailed(f'Error fetching User details : {error}')

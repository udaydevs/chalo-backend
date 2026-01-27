"""Rewriting authenticate function to retrieve the user details"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken


class CookieJWTAuthentication(JWTAuthentication):
    """
    Authenticate JWT from HttpOnly cookie
    """

    def authenticate(self, request):
        token = request.COOKIES.get("access_token")
        if not token:
            return None
        try:
            validated_token = self.get_validated_token(token)
        except InvalidToken as e:
            raise AuthenticationFailed(f"Invalid or expired token: {str(e)}")
        except Exception as e:
            raise AuthenticationFailed(f"Token validation failed: {str(e)}")
        try:
            user = self.get_user(validated_token)
            print(user)
        except AuthenticationFailed as exc:
            raise AuthenticationFailed(f"User retrieval failed: {exc}")

        return (user, validated_token)

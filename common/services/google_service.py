"""This service is used to retrieve user details from github authentication"""
import requests
from django.conf import settings

def google_user_details(token):
    """This will take access token and fetch user details"""
    print( "token",token)
    user_details = requests.post(
            "https://chalo-backend.onrender.com/dj-rest-auth/social/login/google/",
            json={"access_token": token},
            # timeout=20
        )
    return user_details.json()

def google_access_data(code:str):
    """This will authorize from github and fetch access token"""
    print('code',code)
    token_res = requests.post(
        "https://oauth2.googleapis.com/token",
        headers={"Accept": "application/json"},
        data={
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type":"authorization_code",
            "redirect_uri": settings.GOOGLE_CALLBACK_URL
        },
        # timeout=20
    )
    token_res.raise_for_status()
    return token_res.json().get('access_token')

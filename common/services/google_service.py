"""This service is used to retrieve user details from github authentication"""
import requests
from django.conf import settings


def google_user_details(token):
    """This will take access token and fetch user details"""
    user_details = requests.post(
        "http://localhost:8000/dj-rest-auth/social/login/google/",
        json={"access_token": token},
        timeout=20
    )
    print(user_details)
    user_details.raise_for_status()
    return {'msg' : 'Logged In Successfully'}


def google_access_data(code:str):
    """This will authorize from github and fetch access token"""
    print(code)
    token_res = requests.post(
        "https://oauth2.googleapis.com/token",
        headers={"Accept": "application/json"},
        data={
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": code,
        },
        timeout=20
    )
    print(token_res.json().get('access_token'))
    token_res.raise_for_status()
    return token_res.json().get('access_token')

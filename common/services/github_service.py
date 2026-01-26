"""This service is used to retrieve user details from github authentication"""
import requests
from django.conf import settings


def github_user_details(token):
    """This will take access token and fetch user details"""
    user_details = requests.post(
        "https://chalo-backend.onrender.com/dj-rest-auth/social/login/github/",
        json={"access_token": token},
        # timeout=20
    )
    user_details.raise_for_status()
    return {'msg' : 'Logged In Successfully'}


def github_access_data(code:str):
    """This will authorize from github and fetch access token"""
    print(code)
    token_res = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
        },
        # timeout=20
    )
    token_res.raise_for_status()
    return token_res.json().get('access_token')

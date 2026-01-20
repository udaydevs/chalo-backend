"""This service is used to retrieve user details from github authentication"""
import requests
from django.conf import settings


def github_user_details(token):
    """This will take access token and fetch user details"""
    print(token)
    user_details = requests.get(
        url="https://api.github.com/user",
        headers={
            'Authorization' : f'Bearer {token.get('access_token')}',
            "Accept": "application/json",
        },
        timeout=20
    )
    user_details.raise_for_status()
    print(user_details.json())
    return user_details.json()
def github_access_data(code:str):
    """This will authorize from github and fetch access token"""
    print(code)
    token_response = requests.post(
        url='https://github.com/login/oauth/access_token',
        headers={
            'Accept': 'application/json'
        },
        data={
            'client_id' :settings.GITHUB_CLIENT_ID,
            'client_secret' : settings.GITHUB_CLIENT_SECRET,
            'code' : code
        },
        timeout=20
    )
    token_response.raise_for_status()
    return token_response.json()

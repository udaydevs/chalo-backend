"""Users Authentication views"""
# pylint: disable=E1101

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.http import Http404
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from apps.users.api.serializers import (
    LoginUserSerializer,
    OTPVerificationSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
    RegistrationSerializer,
    UserSerializer,
)
from common.services.github_service import github_access_data, github_user_details
# from common.services.google_service import google_access_data, google_user_details
from config import settings
CustomUser = get_user_model()


class Registration(APIView):
    """
    User details and creation takes place here
    """
    def post(self, request):
        """
        User post request for registration
        """
        serializer = RegistrationSerializer(data  = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' : 'Registered Successfully' }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GitHubRegistration(APIView):
    """
    User details and creation takes place using github
    """
    def post(self, request):
        """
        User registeration with github
        """
        code = request.data.get("code")
        data =github_user_details(github_access_data(code))
        if data:
            return Response({'msg' : 'Logged In Successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error' : 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

# class GoogleRegistration(APIView):
#     """
#     User details and creation takes place using github
#     """
#     def post(self, request):
#         """
#         User registeration with github
#         """
#         code = request.data.get("code")
#         print(code)
#         access_token = google_access_data(code)
#         request.data.update({'access_token': access_token})
#         login_view = GoogleLogin.as_view()
#         response= login_view(request._request)
#         print(response)
#         # return response
#         # data =google_user_details(google_access_data(code))
#         if response:
#             return Response({'msg' : 'Logged In Successfully'}, status=status.HTTP_201_CREATED)
#         return Response({'error' : 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    """Login for user"""
    def post(self, request):
        """Post request for authentication"""
        serializer = LoginUserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token = RefreshToken.for_user(user)
            response =Response({'msg' : 'Logged In Successfully' }, status=status.HTTP_201_CREATED)
            response.set_cookie(
                    key="access_token",
                    value=str(token.access_token),
                    httponly=True,
                    secure=True,
                    samesite="None"
                )
            response.set_cookie(
                    key="refresh_token",
                    value=str(token),
                    httponly=True,
                    secure=True,
                    samesite="None"
                )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogOut(APIView):
    """
    LogOut for user
    """
    def post(self, request):
        """
        Docstring for post
        
        :param self: Description
        :param request: Description
        """
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
            except Exception as error:
                return Response(
                    {'error' : 'Error invalidating token :' + str(error)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        response = Response({"msg" : "Successfully logged out!"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

class UserDetails(APIView):
    """Options that are performed on a single user """

    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        """User details from db if exist"""
        data = CustomUser.objects.filter(id = pk)
        if data.exists():
            return data
        else:
            raise Http404

    def get(self, request):
        """Get request for user details"""
        user = self.get_object(pk= request.user.id)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Updation of user fields"""

        user = self.get_object(pk= request.user.id)
        serializer = UserSerializer(user, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequest(APIView):
    """
    User details and creation takes place here
    """
    def post(self, request):
        """
        User post request for registration
        """
        serializer = PasswordResetRequestSerializer(data  = request.data)
        if serializer.is_valid():
            return Response({
                'msg' : 'OTP sent successfully!' ,
                "reset_id" : serializer.data.values()
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerification(APIView):
    """
    User details and creation takes place here
    """
    def post(self, request):
        """
        User post request for registration
        """
        serializer = OTPVerificationSerializer(data  = request.data)
        if serializer.is_valid():
            return Response({'msg' : 'Otp verification successfully' }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordReset(APIView):
    """
    User details and creation takes place here
    """
    def post(self, request):
        """
        User post request for registration
        """
        print(request.data)
        serializer = PasswordResetSerializer(data  = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' : 'Password reset successfully' }, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GitHubLogin(SocialLoginView):
    """This will help to take access token from github and register user"""
    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.GITHUB_CALLBACK_URL

# class GoogleRegistration(SocialLoginView):
    # adapter_class = GoogleOAuth2Adapter
    # client_class = OAuth2Client
    # callback_url = settings.GOOGLE_CALLBACK_URL

    # def post(self, request, *args, **kwargs):
    #     code = request.data.get("code")
    #     if not code:
    #         return Response({'error': 'Code is required'}, status=status.HTTP_400_BAD_REQUEST)
            #     google_data = google_access_data(code)
    #     access_token = google_data.get('access_token')

    #     if hasattr(request.data, '_mutable'):
    #         request.data._mutable = True

    #     request.data['access_token'] = access_token

    #     self.serializer = self.get_serializer(data=request.data)
    #     self.serializer.is_valid(raise_exception=True)

    #     adapter = self.adapter_class(self.request)
    #     app = adapter.get_app(self.request)
    #     token = adapter.parse_token({'access_token': access_token})
    #     token.token_secret = google_data.get('id_token') # Store id_token here

    #     login = adapter.complete_login(request, app, token, response=google_data)
    #     login.token = token
    #     login.state = SocialLoginView.get_social_login(adapter, app, token, google_data)
    #     return super().post(request, *args, **kwargs)

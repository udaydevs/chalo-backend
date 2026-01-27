"""User related Serializers"""
# pylint: disable=E1101
from datetime import datetime
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from common.services.email_service import send_reset_otp

CustomUser = get_user_model()



class RegistrationSerializer(serializers.ModelSerializer):
    """Registration for user serializer"""
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        """Defining the attribute of registration serializer"""
        exclude = ['groups', 'is_active','user_permissions']
        model = CustomUser
        extra_kwargs = {
            'password': {"read_only" : True}

        }
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('confirm_password')
        email = attrs.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("An user with this email already exists!")

        if password != password2:
            raise serializers.ValidationError({
                "status": "error", 
                "Message": "Password and Confirm Password Doesn't Match"
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """User details serializer"""
    class Meta:
        """Only important fields """
        exclude = ['is_staff','is_superuser', 'id','date_joined','status',
                'last_login','password', 'groups', 'user_permissions','created_at', 'updated_at']
        model = CustomUser
        depth = 1

class LoginUserSerializer(serializers.Serializer):
    """Login details serializer"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            return user

        raise serializers.ValidationError("Incorrect credentials!")

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        """This will validate the incoming email and generate a otp and send email to user"""
        try:
            user = CustomUser.objects.get(email = value)
        except CustomUser.DoesNotExist as error:
            raise serializers.ValidationError({
                "error" : "User with this email does not exists.",
                "error_detail" : error
            })
        user.generate_otp()
        send_reset_otp.delay({
            "email": str(user.email),
            "otp": str(user.otp),
            "expiry": str(user.otp_exp),
        })
        return user.id

class OTPVerificationSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    otp = serializers.CharField(max_length = 6)

    def validate(self, attrs):
        try:
            user = CustomUser.objects.get(id = attrs.get('id'))
        except CustomUser.DoesNotExist as error:
            raise serializers.ValidationError({
                "error" : "User with this email does not exists.",
                "error_detail" : error
            })
        if user.otp != attrs.get('otp'):
            raise serializers.ValidationError('Invalid OTP')
        if user.otp_exp < datetime.now():
            raise serializers.ValidationError({
                "error" : 'OTP Expired'
            })
        user.otp_verified = True
        user.save()
        return attrs


class  PasswordResetSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    new_password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)

    def validate(self, attrs):
        try:
            user = CustomUser.objects.get(id = attrs.get('id'))
        except CustomUser.DoesNotExist as error:
            raise serializers.ValidationError({
                "error" : "User with this email does not exists.",
                "error_detail" : error
            })
        if not user.otp_verified:
            raise serializers.ValidationError({
                "error" : 'OTP verification required'
            })
        if attrs.get("new_password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({
                "error" : 'Password and Confirm Password should be same'
            })
        return attrs

    def save(self, *args, **kwargs):
        user  = CustomUser.objects.get(id =self.validated_data.get("id"))
        user.set_password(self.validated_data.get('new_password'))
        user.otp = None
        user.otp_exp = None
        user.verified = False
        user.save()
        return user

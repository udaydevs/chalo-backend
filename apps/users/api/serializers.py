"""User related Serializers"""
# pylint: disable=E1101
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
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

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable

from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = []


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    profile = ProfileSerializer()

    def get_avatar(self, user):
        if user.avatar:
            return user.avatar.content.url
        else:
            return None

    class Meta:
        model = User
        fields = ('suid', 'full_name', 'username', 'is_phone_number_verified', 'phone_number', 'avatar', 'is_guest', 'profile',)


class LoginSerializer(serializers.Serializer):
    user = UserSerializer()
    token = serializers.CharField(required=True)
    refresh = serializers.CharField(required=True)


class UserUpdateSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False)
    avatar = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    is_notification_enabled = serializers.CharField(required=False)


class UserLoginSerializer(serializers.Serializer):
    user = UserSerializer()
    token = serializers.CharField()
    refresh_token = serializers.CharField()


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class PhoneNumberActivationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    activation_code = serializers.CharField()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token

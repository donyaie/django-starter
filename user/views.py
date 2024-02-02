from django.shortcuts import render
from django.utils import timezone
from .serializers import (PhoneNumberSerializer, PhoneNumberActivationSerializer, UserSerializer, UserUpdateSerializer, LoginSerializer)
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager

from .models import User, Profile
from django.utils.translation import gettext
from rest_framework.exceptions import NotAcceptable
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from core.sms import send_verification_sms
from .exceptions import InvalidActivationCodeException
from django.db.transaction import atomic

from drf_yasg.utils import swagger_auto_schema

from contents.models import Image
from core.sms import check_verification
from core.permissions import (
    IsAuthenticatedAndActive, PostOnlyUnAuth, GetOnlyUnAuth)
from rest_framework import status


class UsersView(APIView):
    permission_classes = [IsAuthenticatedAndActive]

    @swagger_auto_schema(responses={status.HTTP_200_OK: UserSerializer(many=False)})
    def get(self, request):
        user = request.user

        serializer = UserSerializer(instance=user)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserUpdateSerializer, responses={status.HTTP_200_OK: UserSerializer(many=False)})
    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        full_name = serializer.validated_data.get('full_name')
        if full_name:
            user.full_name = full_name
            user.save()

        email = serializer.validated_data.get('email')
        if email and email != user.email:
            another_user = User.objects.filter(email=email)
            if another_user.exists():
                raise NotAcceptable(
                    gettext("Another user with this email exists."))
            user.email = email
            user.is_email_verified = False

        avatar = serializer.validated_data.get('avatar')
        with atomic():
            if avatar:
                image = get_object_or_404(Image, suid=avatar, deleted_at__isnull=True)
                user.avatar = image
                image.content_object = user
                image.save()
            user.save()

        

        is_notification_enabled = serializer.validated_data.get(
            'is_notification_enabled')
        if is_notification_enabled:
            user.profile.is_notification_enabled = is_notification_enabled

        user.profile.save()

        user.save()

        serializer = UserSerializer(instance=user)
        return Response(serializer.data)


class AuthPhoneNumberView(APIView):
    permission_classes = (IsAuthenticatedAndActive | PostOnlyUnAuth,)

    @swagger_auto_schema(request_body=PhoneNumberSerializer)
    def post(self, request):

        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')

        num_results = User.objects.filter(phone_number=phone_number).count()

        if num_results > 0:
            user = User.objects.get(phone_number=phone_number)
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
                user.save()

            send_verification_sms(phone_number)
            return Response(serializer.validated_data)

        else:

            password = make_password(BaseUserManager().make_random_password())
            username = uuid.uuid4().hex[:32]

            user = User.objects.create_user(
                username=username, password=password)

            user.phone_number = phone_number
            Profile.objects.create(user=user)
            user.save()

            send_verification_sms(phone_number)

            return Response(serializer.validated_data)


class AuthPhoneNumberActivationView(APIView):
    permission_classes = (IsAuthenticatedAndActive | PostOnlyUnAuth,)

    @swagger_auto_schema(request_body=PhoneNumberActivationSerializer, responses={status.HTTP_200_OK: LoginSerializer(many=False)})
    def post(self, request):
        serializer = PhoneNumberActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get('phone_number')
        code = serializer.validated_data.get('activation_code')

        if not check_verification(phone_number, code):
            raise InvalidActivationCodeException()

        user = User.objects.get(phone_number=phone_number)
        token = RefreshToken.for_user(user)
        user.is_phone_number_verified = True
        user.last_login = timezone.now()
        user.save()
        serializer = UserSerializer(instance=user)
        result = {
            'user': serializer.data,
            'token': str(token.access_token),
            'refresh': str(token)
        }

        return Response(result)

class AuthGuestView(APIView):
    permission_classes = (IsAuthenticatedAndActive | PostOnlyUnAuth,)

    @swagger_auto_schema(responses={status.HTTP_200_OK: LoginSerializer(many=False)})
    def post(self, request):
        password = make_password(BaseUserManager().make_random_password())
        username = 'guest_'+uuid.uuid4().hex[:30]

        user = User.objects.create_user(
            username=username, password=password)
        user.is_guest = True
        user.last_login = timezone.now()
        user.save()
        token = RefreshToken.for_user(user)

        serializer = UserSerializer(instance=user)
        result = {
            'user': serializer.data,
            'token': str(token.access_token),
            'refresh': str(token)
        }
        return Response(result)

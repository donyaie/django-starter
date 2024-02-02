from rest_framework.schemas import get_schema_view
from django.urls import path
from .views import (AuthPhoneNumberView, AuthPhoneNumberActivationView, AuthGuestView, UsersView)


app_name = 'user'


urlpatterns = [
    path('v1/user/', UsersView.as_view(), name='users'),

    path('v1/auth/phone/', AuthPhoneNumberView.as_view(), name='users-auth-phone'),
    path('v1/auth/phone/confirm/', AuthPhoneNumberActivationView.as_view(),name='users-auth-phone-confirm'),
    path('v1/auth/guest/', AuthGuestView.as_view(), name='users-auth-guest'),
]

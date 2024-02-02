from django.urls import path

from .views import (ImagesView, ImageView)

app_name = 'contents'

urlpatterns = [
    path('images/', ImagesView.as_view(), name='images'),
    path('images/<image_suid>/', ImageView.as_view(), name='image'),
]

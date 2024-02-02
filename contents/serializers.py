from rest_framework import serializers

from .models import (Image, Content)


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ('suid', 'content')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        read_only_fields = ('id', 'suid', 'content_object',)
        fields = ('suid', 'created_at', 'content', 'user')
        extra_kwargs = {
            'user': {'write_only': True},
        }

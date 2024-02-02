from django.utils import timezone
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Image
from .serializers import ImageSerializer


class ImagesView(CreateAPIView):
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        return super(ImagesView, self).create(request, *args, **kwargs)


class ImageView(APIView):
    def delete(self, request, image_suid):
        user = request.user
        image = get_object_or_404(Image, user=user, suid=image_suid,deleted_at__isnull=True)
        image.deleted_at = timezone.now()
        image.save()
        serializer = ImageSerializer(instance=image)
        return Response(data=serializer.data)

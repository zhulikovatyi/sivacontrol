from rest_framework import viewsets

from models import Banner, Gender
from serializers import BannerSerializer, GenderSerializer
from .tasks import move_video, remove_video
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def create(self, request, *args, **kwargs):
        self.file_name = default_storage.save(request.data['video'].name.replace(' ', '_'), ContentFile(request.data['video'].read()))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        super(VideoViewSet, self).perform_create(serializer)
        url = serializer.data['url']
        move_video.delay(settings.MEDIA_ROOT+self.file_name, serializer.data['id'])

    def perform_destroy(self, instance):
        movie_name = instance.url.split('/')[-1]
        instance.delete()
        remove_video.delay(movie_name)


class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
from rest_framework import viewsets

from models import Banner, Gender
from serializers import BannerSerializer, GenderSerializer
from .tasks import move_video
from django.conf import settings

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def perform_create(self, serializer):
        super(VideoViewSet, self).perform_create(serializer)
        url = serializer.data['url']
        move_video.delay(settings.MEDIA_ROOT+url.split('/')[-1], serializer.data['id'])
        pass


class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
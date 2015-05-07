from rest_framework import viewsets
from rest_framework import filters

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
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('id',)
    ordering = ('-id',)

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

    def update(self, request, *args, **kwargs):
        print 'file' in request.FILES, request.FILES, request.FILES['file'].name
        return Response({})
        self.file_name = None
        if 'file' in request.FILES:
            self.file_name = default_storage.save(request.data['video'].name.replace(' ', '_'), ContentFile(request.data['video'].read()))
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        self.old_file_name = instance.url
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        super(VideoViewSet, self).perform_update(serializer)
        if self.file_name is not None:
            move_video.delay(settings.MEDIA_ROOT+self.file_name, serializer.data['id'])
            remove_video.delay(self.old_file_name)


class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
from kombu import mixins
from rest_framework import viewsets, mixins
from rest_framework import filters, decorators, response

from models import Banner, Gender, AgeGroup, BannerWeight
from serializers import BannerSerializer, GenderSerializer, AgeGroupSerializer, BannerWeightSerializer
from .tasks import move_video, remove_video
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os, uuid

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('id',)
    ordering = ('-id',)

    def create(self, request, *args, **kwargs):
        file_name, extension = os.path.splitext(request.data['video'].name)
        self.file_name = default_storage.save(str(uuid.uuid4())+extension,
                                              ContentFile(request.data['video'].read()))
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
        self.file_name = None
        if 'file' in request.FILES:
            print request.META['HTTP_X_FILE_NAME']
            file_name, extension = os.path.splitext(request.META['HTTP_X_FILE_NAME'])
            self.file_name = default_storage.save(str(uuid.uuid4())+extension,
                                                  ContentFile(request.FILES['file'].read()))
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        self.old_file_name = instance.url.split('/')[-1]
        if self.file_name is not None:
            instance.url = 'Coming soon ...'
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception='file' not in request.FILES)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        if self.file_name is not None:
            move_video.delay(settings.MEDIA_ROOT+self.file_name, serializer.instance.id)
            remove_video.delay(self.old_file_name)
        else:
            super(VideoViewSet, self).perform_update(serializer)



class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer


class BannerWeightViewSet(viewsets.ModelViewSet):
    queryset = BannerWeight.objects.all()
    serializer_class = BannerWeightSerializer

    @decorators.detail_route(methods=['get', ])
    def values(self, request):
        resp = [{'key': item[0], 'label': item[1]} for item in BannerWeight.BANNER_WEIGHTS]
        return response.Response(resp)


class AgeGroupViewSet(viewsets.ModelViewSet):
    queryset = AgeGroup.objects.all()
    serializer_class = AgeGroupSerializer
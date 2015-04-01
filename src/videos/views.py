from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from models import Banner, Gender
from serializers import BannerSerializer, GenderSerializer

class VideoList(APIView):

    def get(self, request, format=None):
        videos = Banner.objects.all()
        serializer = BannerSerializer(videos, many=True)
        return Response(serializer.data)
        pass

    def post(self, request, format=None):
        pass

class VideoDetail(APIView):

    def get(self, request, pk, format=None):
        videos = Banner.objects.all()
        serializer = BannerSerializer(videos, many=True)
        return Response(serializer.data)
        pass

    def put(self, request, pk, format=None):
        pass

    def delete(self, request, pk, format=None):
        pass
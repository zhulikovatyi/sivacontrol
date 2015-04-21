from django.forms import widgets
from rest_framework import serializers
from models import Banner, Gender

class BannerSerializer(serializers.ModelSerializer):
    genders = serializers.PrimaryKeyRelatedField(many=True, queryset=Gender.objects.all())
    class Meta:
        model = Banner
        fields = ('id', 'title', 'url', 'genders', 'is_active')

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ('id', 'title')
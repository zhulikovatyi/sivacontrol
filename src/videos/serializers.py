from rest_framework import serializers
from models import Banner, Gender, BannerWeight, AgeGroup

class BannerWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerWeight
        fields = ('id', 'banner', 'age_group', 'gender', 'weight')

class BannerSerializer(serializers.ModelSerializer):
    age_gender_weights = BannerWeightSerializer(many=True)
    class Meta:
        model = Banner
        fields = ('id', 'title', 'url', 'is_active', 'age_gender_weights')


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ('id', 'title')




class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroup
        field = ('id', 'start_boundary', 'stop_boundary')
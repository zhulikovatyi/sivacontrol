from __future__ import absolute_import
from celery import shared_task
from .models import Banner
from django.conf import settings
import requests
import os


@shared_task
def move_video(path_to_video, identity):
    f = open(path_to_video)
    r = requests.post(
        settings.STREAM_API+"/movie",
        files={'movie': f}
    )
    json = r.json()
    url = json['url']
    result = Banner.objects.filter(pk=int(identity)).update(
        url=url,
        is_active=True
    )
    os.remove(path_to_video)
    return result


@shared_task
def remove_video(video_name):
    r = requests.delete(
        settings.STREAM_API+"/movie",
        data={
            'movie_name': video_name
        }
    )
    return r
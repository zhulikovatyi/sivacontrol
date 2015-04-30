from __future__ import absolute_import
from celery import shared_task
from .models import Banner
import requests
import os

@shared_task
def move_video(path_to_video, identity):
    r = requests.post(
        "http://192.168.1.78:8888/movie",
        files={'movie': open(path_to_video)}
    )
    json = r.json()
    url = json['url']
    result = Banner.objects.filter(pk=int(identity)).update(
        url=url,
        is_active=True
    )
    os.remove(path_to_video)
    return result
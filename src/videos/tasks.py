from __future__ import absolute_import
from celery import shared_task
from .models import Banner
from django.utils.crypto import get_random_string

import subprocess
import os

@shared_task
def move_video(path_to_video, identity):
    # move file to video streaming server through ssh
    # TODO implement this feature through mounted disk
    name = path_to_video.replace(' ', '_').split('/')[-1]
    name_without_extension, extension = name.split('.')[:-1][0], name.split('.')[-1]
    new_name = name_without_extension+"_"+get_random_string(length=32)+"."+extension
    subprocess.call(['scp', path_to_video, 'slava@192.168.1.78:/var/mp4s/'+new_name])
    result = Banner.objects.filter(pk=int(identity)).update(
        url="rtmp://192.167.1.78:1935/vod2/"+new_name,
        is_active=True
    )
    os.remove(path_to_video)
    return result


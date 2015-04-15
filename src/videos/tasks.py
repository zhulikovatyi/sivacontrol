from __future__ import absolute_import
from celery import shared_task
from .models import Banner

import subprocess


@shared_task
def move_video(path_to_video, identity):
    # move file to video streaming server through ssh
    # TODO implement this feature through mounted disk
    subprocess.call(['scp', path_to_video, 'slava@192.168.1.78:/var/mp4s'])
    return Banner.objects.filter(pk=int(identity)).update(
        url="rtmp://192.168.1.78/vod2/"+path_to_video.split('/')[-1],
        is_active=True
    )


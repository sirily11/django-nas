import ffmpeg
import os
from os.path import dirname, join, splitext, exists, basename
from django_rq import job
import time
from django.conf import settings

@job
def transcode_video(path: str):
    name = f"{splitext(basename(path))[0]}.m3u8"
    t_p = f"{splitext(path)[0]}_transcode"
    output_path = join(settings.MEDIA_ROOT, t_p, name)
    if not exists(t_p):
        os.mkdir(t_p)
    stream = ffmpeg.input(path)
    stream = ffmpeg.output(stream, output_path)
    ffmpeg.run(stream)
    return output_path

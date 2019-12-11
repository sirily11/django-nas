import ffmpeg
import os
from os.path import dirname, join, splitext, exists, basename


def transcode_video(path: str):
    name = f"{splitext(basename(path))[0]}.m3u8"
    t_p = f"{splitext(path)[0]}_transcode"
    output_path = join(t_p, name)
    if not exists(t_p):
        os.mkdir(t_p)
    stream = ffmpeg.input(path)
    stream = ffmpeg.output(stream, output_path)
    ffmpeg.run(stream)
    return output_path


print(splitext("/Users/liqiwei/Desktop/projects/django_nas/django_nas/media/Screen_Shot_2019-12-07_at_9.09.29_PM.png")[1])

import os
from os.path import dirname, join, splitext, exists, basename
from django.conf import settings

AUDIO_EXT = ['.m4a', '.wav', '.mp3']
VIDEO_EXT = ['.m4v', '.mov', '.m4a', '.wmv', '.mp4', '.avi', '.m3u8']

"""
This file contains utils which don't use model
"""


def is_video(path: str) -> bool:
    """
    Whether a file is video
    :param path:
    :return:
    """
    filename, file_ext = os.path.splitext(path)
    if file_ext.lower() in VIDEO_EXT:
        return True
    return False


def is_audio(path: str) -> bool:
    """
    Whether a file is audio
    :param path:
    :return:
    """
    filename, file_ext = os.path.splitext(path)
    if file_ext.lower() in AUDIO_EXT:
        return True

    return False


def get_filename(path, file_id) -> (str, str):
    """
    Get video cover file name
    :param path:
    :param file_id:
    :return:
    """
    name = f"{file_id}-{splitext(basename(path))[0]}.jpg"
    output_path = join(settings.MEDIA_ROOT, "covers", name)
    return name, output_path


def get_video_filename(path, file_id) -> (str, str):
    """
    Get transcode video name
    :param path:
    :param file_id:
    :return:
    """
    name = f"{file_id}-{splitext(basename(path))[0]}.mp4"
    output_path = join(settings.MEDIA_ROOT, "transcode-video", name)
    return name, output_path

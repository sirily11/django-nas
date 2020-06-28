import os
from os.path import dirname, join, splitext, exists, basename
from django.conf import settings

IMAGE_EXT = ['.jpg', 'jpeg', '.png', '.bmp']
AUDIO_EXT = ['.m4a', '.wav', '.mp3']
VIDEO_EXT = ['.m4v', '.mov', '.m4a', '.wmv', '.mp4', '.avi', '.m3u8']
DOCUMENT_EXT = ['.pdf', '.txt', '.docx', '.csv', '.epub', '.pptx', '.xls', 'xlsx', '.html', '.srt']

"""
This file contains utils which doesn't use model
"""


def is_image(path: str) -> bool:
    """
      Whether a file is image
      :param path:
      :return:
      """
    filename, file_ext = os.path.splitext(path)
    if file_ext.lower() in IMAGE_EXT:
        return True
    return False


def is_document(path: str) -> bool:
    """
    Whether a file is video
    :param path:
    :return:
    """
    filename, file_ext = os.path.splitext(path)
    if file_ext.lower() in DOCUMENT_EXT:
        return True
    return False


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


class WebVTTWriter(object):

    def write(self, captions):
        content = 'WEBVTT\n'
        for c in captions:
            if c.identifier:
                content += '\n' + c.identifier
            content += '\n{} --> {}\n'.format(c.start, c.end)
            for l in c.lines:
                content += '{}\n'.format(l)
        return content

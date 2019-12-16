from django.db import models
from django.contrib.auth.models import User
import django_rq
import os
import ffmpeg
from os.path import dirname, join, splitext, exists, basename
from django_rq import job
from django.conf import settings
from django.db.models import Sum

CHOICES = (("Image", "image"), ("Text", "txt"), ("File", "file"))
VIDEO_EXT = ['.m4v', '.mov', '.m4a', '.wmv', '.mp4']


def user_directory_path(instance, filename: str):
    path = filename
    p = instance.parent
    print(filename)

    while p:
        path = join(p.name, path)
        p = p.parent

    return path


class Folder(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="folders", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, default="")
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    size = models.FloatField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_size(self):
        """
        Get total size for the current directory in bytes
        :return:
        """
        total_size = File.objects.filter(parent=self.pk).aggregate(Sum('size'))['size__sum']
        folders = Folder.objects.filter(parent=self.pk).all()

        for folder in folders:
            total_size += folder.total_size

        return total_size

    def parents(self):
        """
        Get parents of current dir. If current dir is root, then menu is []. The menus will include self
        :return:
        """
        folder = Folder.objects.get(pk=self.pk)
        p = folder
        menus = []
        while p:
            menus.append({"name": p.name, "id": p.id})
            p = p.parent

        menus.reverse()
        return menus

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("parent", "name")


class File(models.Model):
    object_type = models.CharField(choices=CHOICES, max_length=128, default="file")
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    size = models.FloatField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="files", null=True, blank=True)
    file = models.FileField(upload_to=user_directory_path)
    transcode_filepath = models.FileField(null=True, blank=True)
    cover = models.FileField(null=True, blank=True)

    def filename(self):
        return self.file.name

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs) -> None:
        size = self.file.size
        self.size = size
        filename, file_extension = os.path.splitext(self.file.path)
        super(File, self).save(*args, **kwargs)

        if file_extension.lower() in VIDEO_EXT and self.cover.name is None:
            queue = django_rq.get_queue()
            queue.enqueue(generate_video_cover, self.file.path, self.pk)

    def delete(self, *args, **kwargs):
        _, output_path = get_filename(self.file.path, self.id)
        if exists(output_path):
            os.remove(output_path)
        super(File, self).delete(*args, **kwargs)


class Document(models.Model):
    content = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="documents", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, default="")
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    size = models.FloatField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True)


def get_filename(path, file_id) -> (str, str):
    name = f"{file_id}-{splitext(basename(path))[0]}.jpg"
    output_path = join(settings.MEDIA_ROOT, "covers", name)
    return name, output_path


@job
def transcode_video(path, file_id):
    name, output_path = get_filename(path, file_id)
    file = File.objects.filter(pk=file_id).first()
    if not exists(join(settings.MEDIA_ROOT, "transcodes")):
        os.mkdir(join(settings.MEDIA_ROOT, "transcodes"))
    stream = ffmpeg.input(path)

    stream = ffmpeg.output(stream, output_path)
    ffmpeg.run(stream)
    file.transcode_filepath.name = join("transcodes", name)
    file.save()
    return output_path


@job
def generate_video_cover(path, file_id):
    name, output_path = get_filename(path, file_id)
    file = File.objects.filter(pk=file_id).first()
    if not exists(join(settings.MEDIA_ROOT, "covers")):
        os.mkdir(join(settings.MEDIA_ROOT, "covers"))
    if not exists(output_path):
        stream = ffmpeg.input(path)
        stream = ffmpeg.filter(stream, 'scale', 1920, -1)
        stream = ffmpeg.output(stream, output_path, vframes=1)
        ffmpeg.run(stream)
        file.cover.name = join("covers", name)
        file.save()
    return output_path

from django.db import models
from django.contrib.auth.models import User
import django_rq
import os
import ffmpeg
from os.path import join, exists
from django_rq import job
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from nas.utils.utils2 import is_video, is_audio, get_filename, get_video_filename, is_document

CHOICES = (("Image", "image"), ("Text", "txt"), ("File", "file"))
EVENT_TYPES = (("CREATED", "created"), ("DELETED", "deleted"),
               ("UPDATED", "updated"), ("LOG", "log"))


# Generate file path based on its parent
def user_directory_path(instance, filename: str):
    path = filename
    p = instance.parent

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
    size = models.FloatField(blank=True, null=True, default=0)
    modified_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_size(self):
        files = File.objects.filter(parent=self.pk).all()
        folders = Folder.objects.filter(parent=self.pk).all()
        total_size = 0
        for file in files:
            total_size += file.size

        for folder in folders:
            if folder.size:
                total_size += folder.size

        return total_size

    @property
    def calculate_total_size(self):
        """
        Get total size for the current directory in bytes
        :return:
        """
        files = File.objects.filter(parent=self.pk).all()
        folders = Folder.objects.filter(parent=self.pk).all()

        total_size = sum(f.size for f in files if f.size)
        for folder in folders:
            total_size += folder.calculate_total_size

        self.size = total_size
        self.save()
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


class File(models.Model):
    object_type = models.CharField(choices=CHOICES, max_length=128, default="file")
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    size = models.FloatField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="files", null=True, blank=True)
    file = models.FileField(upload_to=user_directory_path, max_length=1000000)
    transcode_filepath = models.FileField(null=True, blank=True)
    cover = models.FileField(null=True, blank=True)
    has_uploaded_to_cloud = models.BooleanField(default=False, null=True, blank=True)

    def filename(self):
        return os.path.basename(self.file.name)

    def relative_filename(self, until: int) -> str:
        """
        Get relative filename. For example if a file path is a/b/c.pdf,
        and until is a, this will return b/c.pdf
        :param until:
        :return:
        """
        parent = self.parent
        filename = os.path.basename(self.file.name)
        while parent:
            if parent.id == until:
                break
            filename = os.path.join(parent.name, filename)
            parent = parent.parent
        return filename

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs) -> None:
        folder = None
        # If no file upload
        if not self.file:
            super(File, self).save(*args, **kwargs)
            return

        size = self.file.size
        self.size = size

        if self.parent:
            folder = Folder.objects.get(id=self.parent.id)

        self.modified_at = timezone.now()
        super(File, self).save(*args, **kwargs)

        if folder:
            if folder.size:
                folder.size += size
            else:
                folder.size = size
            folder.save()

        if is_video(self.file.path) and self.cover.name is None:
            # If file is video
            queue = django_rq.get_queue()
            queue.enqueue(generate_video_cover, self.file.path, self.pk)
            if settings.TRANSCODE_VIDEO:
                queue.enqueue(transcode_video, self.file.path, self.pk)

        if is_audio(self.file.name):
            from nas.utils.utils import get_and_create_music_metadata
            get_and_create_music_metadata(self)

        if is_document(self.file.name):
            from nas.utils.utils import extra_text_content
            content = extra_text_content(self)
            self.description = content
            super().save()

    def delete(self, *args, **kwargs):
        folder = None
        _, output_path = get_filename(self.file.path, self.id)
        if exists(output_path):
            os.remove(output_path)
        if self.parent:
            folder = Folder.objects.get(id=self.parent.id)
        super(File, self).delete(*args, **kwargs)
        if folder:
            if folder.size:
                folder.size -= self.size
            else:
                folder.size = 0
            folder.save()


class MusicMetaData(models.Model):
    file = models.OneToOneField(File, on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                related_name="metadata",
                                )
    title = models.CharField(blank=True, null=True, max_length=1024)
    album = models.CharField(blank=True, null=True, max_length=1024)
    artist = models.TextField(blank=True, null=True, max_length=1024)
    album_artist = models.TextField(blank=True, null=True, max_length=1024)
    year = models.CharField(default='2020', max_length=128)
    track = models.IntegerField(default=0)
    genre = models.CharField(null=True, blank=True, max_length=128)
    picture = models.FileField(upload_to='music-cover/%Y/%m/%d', null=True, blank=True)
    duration = models.IntegerField(blank=True, null=True)
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class BookCollection(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    content = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE,
                               related_name="documents",
                               null=True,
                               blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, default="")
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    size = models.FloatField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    show_in_folder = models.BooleanField(default=True)
    collection = models.ForeignKey(to=BookCollection, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="books")

    def __str__(self):
        return self.name


class Logs(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=1024, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    sender = models.CharField(max_length=128, default="system")
    log_type = models.CharField(choices=EVENT_TYPES, null=False, blank=False, max_length=128)

    def __str__(self):
        return self.title


@job
def transcode_video(path, file_id):
    name, output_path = get_video_filename(path, file_id)
    file = File.objects.filter(pk=file_id).first()
    if not exists(join(settings.MEDIA_ROOT, "transcode-video")):
        os.mkdir(join(settings.MEDIA_ROOT, "transcode-video"))
    stream = ffmpeg.input(path)
    stream = ffmpeg.output(stream, output_path, pix_fmt='yuv420p', s="1920x1080", a="aac")
    ffmpeg.run(stream)
    file.transcode_filepath.name = join("transcode-video", name)
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

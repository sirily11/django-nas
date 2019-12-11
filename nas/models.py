from typing import Optional, Union, Sequence
from django.db import models
from django.contrib.auth.models import User
from os.path import join
# from .video_transcode import transcode_video
# import django_rq

CHOICES = (("Image", "image"), ("Text", "txt"), ("File", "file"))
VIDEO_EXT = ['.m4v', '.mov', '.mp4', '.m4a', '.wmv']

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
        files = File.objects.filter(parent=self.pk).all()
        folders = Folder.objects.filter(parent=self.pk).all()

        total_size = sum(f.size for f in files if f.size)
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

    def filename(self):
        return self.file.name

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs) -> None:
        size = self.file.size
        self.size = size
        if self.file.path.lower() in VIDEO_EXT:
            transcode_video(self.file.path)

        super(File, self).save(*args, **kwargs)


class Document(models.Model):
    content = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="documents", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, default="")
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    size = models.FloatField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True)


# def transcode_video(sender: File, **kwargs):
#     if kwargs['created']:
#         print("Created")
#         print(sender.file.url)
#
#
# post_save.connect(transcode_video, sender=File)

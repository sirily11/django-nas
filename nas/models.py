from django.db import models
from django.contrib.auth.models import User
from os.path import join

CHOICES = (("Image", "image"), ("Text", "txt"), ("File", "file"))


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
    name = models.CharField(max_length=128, unique=True, default="")
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.FloatField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class File(models.Model):
    object_type = models.CharField(choices=CHOICES, max_length=128, default="file")
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.FloatField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="files", null=True, blank=True)
    file = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return self.file.name

from .models import File, Folder
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class FileSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="owner")

    class Meta:
        model = File
        fields = ("id","created_at", "description", "user", "size", "modified_at", "file", "object_type")


class FolderBasicSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="owner")

    class Meta:
        model = Folder
        fields = ("id","created_at", "name", "description", "user", "size", "modified_at")


class FolderSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="owner", read_only=True, required=False)
    files = FileSerializer(many=True, read_only=True)
    folders = FolderBasicSerializer(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = ("id", "created_at", "name", "description", "user", "size", "modified_at", "files", "folders")

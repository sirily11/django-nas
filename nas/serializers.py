from .models import File, Folder, Document
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class FileSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="owner", read_only=True)
    filename = serializers.ReadOnlyField()

    class Meta:
        model = File
        fields = ("id", "created_at", "parent",
                  "description", "user", "size",
                  "modified_at", "file", "object_type", "filename", "transcode_filepath")


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("id", "created_at", "name",
                  "description", "size",
                  "modified_at", "parent", "content")


class DocumentAbstractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("id", "created_at", "name",
                  "description", "size",
                  "modified_at", "parent")


class FolderBasicSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="owner")
    parents = serializers.ReadOnlyField()
    total_size = serializers.ReadOnlyField()

    class Meta:
        model = Folder
        fields = ("id", "created_at", "name",
                  "description", "user", "size",
                  "modified_at", "parents", "total_size")


class FolderSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="owner", read_only=True, required=False)
    files = FileSerializer(many=True, read_only=True)
    folders = FolderBasicSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    parents = serializers.ReadOnlyField()
    total_size = serializers.ReadOnlyField()

    class Meta:
        model = Folder
        fields = (
            "id", "created_at", "name",
            "parent", "description",
            "user", "size", "modified_at",
            "files", "folders", "parents",
            "documents", "total_size")

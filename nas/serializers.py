from rest_framework.response import Response

from .models import File, Folder, Document, MusicMetaData, Logs, BookCollection
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import pagination
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class BookCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCollection
        fields = ("id", "name", "description", "created_time")


class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = ("id", "title", "time", "content", "log_type", "sender")


class MusicMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicMetaData
        fields = ("id", "title", "album", "artist",
                  "year", "genre", "track",
                  "picture", "duration", "file", "like", 'album_artist')


class FileSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="owner", read_only=True)
    filename = serializers.ReadOnlyField()
    music_metadata = MusicMetaDataSerializer(source="metadata", read_only=True, many=False)

    class Meta:
        model = File
        fields = ("id", "created_at", "parent",
                  "description", "user", "size",
                  "modified_at", "file", "object_type", "filename", "transcode_filepath", 'cover',
                  'has_uploaded_to_cloud', "music_metadata")


class DocumentSerializer(serializers.ModelSerializer):
    book_collection = BookCollectionSerializer(many=False, source="collection", read_only=True)

    class Meta:
        model = Document
        fields = ("id", "created_at", "name",
                  "description", "size",
                  "modified_at", "parent", "content", "collection", "book_collection", "show_in_folder")


class DocumentAbstractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("id", "created_at", "name",
                  "description", "size",
                  "modified_at", "parent", "show_in_folder", "collection")


class BookCollectionDetailSerializer(serializers.ModelSerializer):
    documents = DocumentAbstractSerializer(source="books", many=True)

    class Meta:
        model = BookCollection
        fields = ("id", "name", "description", "created_time", "documents")


class FolderBasicSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="owner")
    parents = serializers.ReadOnlyField()
    total_size = serializers.ReadOnlyField()

    class Meta:
        model = Folder
        fields = ("id", "created_at", "name",
                  "description", "user", "size",
                  "modified_at", "parents", "total_size", "parent")


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


class NumPagePagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "results": data
        })

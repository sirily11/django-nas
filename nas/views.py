import json
from typing import Optional
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.db.models import Q
from django.shortcuts import HttpResponse
from django.http import JsonResponse

from nas.utils.utils import get_list_files, has_parent, create_folders
from .serializers import FolderSerializer, \
    FileSerializer, UserSerializer, FolderBasicSerializer, DocumentSerializer, \
    DocumentAbstractSerializer, NumPagePagination, MusicMetaDataSerializer, \
    LogsSerializer, BookCollectionSerializer, BookCollectionDetailSerializer
from .models import Folder, File, Document, MusicMetaData, Logs, BookCollection, ImageMetaData
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics
import psutil
from django.conf import settings
import os
from pathlib import PurePath
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import filters
from django_rq import job
import django_rq
import zipstream
from django.http import StreamingHttpResponse
from nas.utils.utils import get_and_create_music_metadata, extra_text_from_current_files
from datetime import datetime
from time import time
import webvtt

from .utils.image_utils import get_image_metadata


class BookCollectionViewSet(viewsets.ModelViewSet):
    queryset = BookCollection.objects.all()
    serializer_class = BookCollectionSerializer
    pagination_class = None

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = BookCollectionDetailSerializer
        return super().retrieve(request, *args, **kwargs)


# from .documents import DocDocument
class LogsViewSet(viewsets.ModelViewSet):
    queryset = Logs.objects.order_by("-time").all()
    serializer_class = LogsSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


class MusicMetaDataViewSet(viewsets.ModelViewSet):
    queryset = MusicMetaData.objects.all()
    serializer_class = MusicMetaDataSerializer


@method_decorator(csrf_exempt, name='dispatch')
class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def create(self, request, *args, **kwargs):
        parent = request.data.get('parent')
        name = request.data.get("name")
        if parent == "":
            parent = None

        query = Folder.objects.filter(parent_id=parent, name=name)
        if query.exists():
            serializer = FolderSerializer(query.first())
            return Response(data=serializer.data, status=200)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        try:
            queue = django_rq.get_queue()
            queue.enqueue(update_total_size)
        except Exception:
            pass
        return res

    def list(self, request, *args, **kwargs):
        # Get root
        obj = Folder.objects.filter(parent__isnull=True).all()
        obj2 = File.objects.filter(parent__isnull=True).all()
        obj3 = Document.objects.filter(parent__isnull=True, show_in_folder=True).all()

        total_size = sum(o.total_size for o in obj)
        total_size += sum(o.size for o in obj2 if o.size)

        serializer = FolderBasicSerializer(obj, many=True)
        serializer2 = FileSerializer(obj2, many=True, context={'request': request})
        serializer3 = DocumentAbstractSerializer(obj3, many=True)

        try:

            return Response(data={
                "name": "root",
                "folders": serializer.data,
                "files": serializer2.data,
                "documents": serializer3.data,
                "parents": [],
                "total_size": total_size
            },
                status=200)
        except Exception:
            return Response(status=500)


class PhotoView(viewsets.ModelViewSet):
    pass


class AlbumView(generics.ListAPIView):
    serializer_class = MusicMetaDataSerializer
    pagination_class = None

    def get_queryset(self):
        artist = self.request.query_params.get('artist')
        album_artist = self.request.query_params.get('album_artist')

        query = MusicMetaData.objects.order_by('album').values('album').distinct()
        if artist:
            query = MusicMetaData.objects.filter(artist=artist).order_by('album').values('album').distinct()

        if album_artist:
            query = MusicMetaData.objects.filter(album_artist=album_artist).order_by('album').values('album').distinct()
        albums = []
        for q in query:
            album = MusicMetaData.objects.filter(album=q['album']).first()
            albums.append(album)
        return albums


class ArtistView(generics.ListAPIView):
    serializer_class = MusicMetaDataSerializer
    pagination_class = None

    def get_queryset(self):
        query = MusicMetaData.objects.order_by('artist').values('artist').distinct()
        artists = []
        for q in query:
            artist = MusicMetaData.objects.filter(artist=q['artist']).first()
            artists.append(artist)

        return artists


class MusicView(generics.ListAPIView, generics.UpdateAPIView):
    serializer_class = FileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['file', 'metadata__title', 'metadata__album', 'metadata__artist']
    pagination_class = NumPagePagination
    page_size = 10

    def update(self, request, *args, **kwargs):
        start_time = datetime.now()
        for file in self.get_queryset():
            get_and_create_music_metadata(file)

        num_music_metadata = MusicMetaData.objects.count()
        content = f"# Music Library has been updated\n\n"
        content += f"User has request the rebuild index at {start_time}. " \
                   f"And during this process, system has updated " \
                   f"{len(self.get_queryset())} music's metadata. " \
                   f"After this operation, the total number of " \
                   f"music metadata is {num_music_metadata}. This update ended at {datetime.now()}\n\n"
        content += f"Author: auto generated logs"

        Logs.objects.create(title="Updated Music Library", content=content, log_type="UPDATED", sender="Music View")
        return Response(data={"update": "ok"}, status=201)

    def get_queryset(self):
        audio_ext = [".m4a", ".mp3"]
        queryset = None
        artist = self.request.query_params.get('artist')
        album = self.request.query_params.get('album')
        like = self.request.query_params.get('like')
        for ext in audio_ext:
            files = File.objects.filter(file__contains=ext).order_by("file").all()
            if not queryset:
                queryset = files
            else:
                queryset = queryset | files

        if artist:
            queryset = queryset.filter(metadata__artist__icontains=artist)

        if album:
            queryset = queryset.filter(metadata__album__icontains=album)

        if like:
            queryset = queryset.filter(metadata__like=True)

        return queryset


@method_decorator(csrf_exempt, name='dispatch')
class FileViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    queryset = File.objects.all()
    serializer_class = FileSerializer
    pagination_class = None
    search_fields = ['file', 'description']

    def create(self, request, *args, **kwargs):
        file: InMemoryUploadedFile = request.data.get("file")
        parent: str = request.data.get("parent")
        parent_folder: Optional[Folder] = None
        if parent:
            parent_folder = Folder.objects.get(id=int(parent))
        paths = request.data.get("paths")

        if file and paths:
            if has_parent(paths):
                paths = list(PurePath(paths).parts)
                base_name, folder = create_folders(paths, parent_folder)
                request.data['parent'] = str(folder.id) if folder else None
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        new_file_name = request.data.get('filename')

        if new_file_name:
            file_id = kwargs.get('pk')
            file: File = File.objects.get(id=file_id)
            original_path = file.file.path
            original_name = file.file.name
            new_path = file.file.path.replace(os.path.basename(original_path), new_file_name)
            new_name = original_name.replace(os.path.basename(original_path), new_file_name)
            file.file.name = new_name
            os.rename(original_path, new_path)
            file.save()
        res = super().update(request, *args, **kwargs)
        try:
            queue = django_rq.get_queue()
            queue.enqueue(update_total_size, request.data['parent'])
        except Exception:
            pass
        return res


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    search_fields = ['content']


@method_decorator(csrf_exempt, name='dispatch')
class SystemInfoView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        try:
            cpu = psutil.cpu_percent()
            # disk = psutil.disk_usage(settings.MOUNT_POINT)
            disk = psutil.disk_usage(os.getcwd())
            memory = psutil.virtual_memory()
            data = {
                "cpu": cpu,
                "disk": {"used": disk.used, "total": disk.total},
                "memory": {"used": memory.used, "total": memory.total}
            }
            return Response(data=data)
        except Exception:
            pass


def index(request):
    try:
        with open(os.path.join(settings.REACT_APP_DIR, 'build', 'index.html')) as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        return HttpResponse(
            """
             Webapp not found
            """,
            status=501,
        )


class FileContentView(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    queryset = File.objects.all()

    def list(self, request, *args, **kwargs):
        return Response(status=405, data=[])

    def retrieve(self, request, *args, **kwargs):
        file: File = self.get_object()
        file_data = self.get_serializer(file)
        try:
            if file and file.file:
                with open(file.file.path, 'rb') as f:
                    content = f.read()
                    data = dict(file_data.data)
                    data['file_content'] = content

                    return Response(status=201, data=data)
        except UnicodeDecodeError as e:
            try:
                with open(file.file.path, 'r', encoding='gb18030') as f:
                    content = f.read()
                    data = dict(file_data.data)
                    data['file_content'] = content

                    return Response(status=201, data=data)
            except Exception as e:
                return Response(status=500, data={"error": str(e)})

    def update(self, request, *args, **kwargs):
        file_content = request.data.get('file_content')
        file: File = self.get_object()
        file_data = self.get_serializer(file)
        try:
            with open(file.file.path, 'w') as f:
                f.write(file_content)
        except Exception as e:
            return Response(data={"error": e}, status=500)
        data = dict(file_data.data)
        data['file_content'] = file_content
        return Response(data=data, status=200)

    def create(self, request, *args, **kwargs):

        body = request.data
        name = body.get('filename')
        file_content = body.get('file_content')
        file_content = file_content if file_content else "None"
        uploaded_file = SimpleUploadedFile(name, bytes(file_content, encoding='utf8'))
        data = dict(request.data)
        data['file'] = uploaded_file
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        resp_data = dict(serializer.data)
        resp_data['file_content'] = file_content
        # clear file content if original content is empty
        if file_content == "None":
            file: File = serializer.instance
            with open(file.file.path, 'w') as f:
                f.write("")
                resp_data['file_content'] = ""

        headers = self.get_success_headers(serializer.data)

        return Response(resp_data, status=201, headers=headers)


class ImageGalleryView(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_queryset(self):
        from nas.utils.utils2 import IMAGE_EXT
        queryset = None

        for ext in IMAGE_EXT:
            files = File.objects \
                .filter(Q(file__contains=ext) | Q(file__contains=ext.upper())) \
                .exclude(image_metadata__data__isnull=True) \
                .all()

            if not queryset:
                queryset = files
            else:
                queryset = queryset | files

        queryset = queryset.order_by("-image_metadata__data__datetime")
        return queryset

    def update(self, request, *args, **kwargs):
        images = self.get_queryset().all()
        for image in images:
            metadata = get_image_metadata(image.file.path)
            if ImageMetaData.objects.filter(file=image).exists():
                ImageMetaData.objects.filter(file=image).delete()
            ImageMetaData.objects.create(file=image, data=metadata)
        return Response(status=201)


@job
def update_total_size(parent=None):
    if not parent:
        folders = Folder.objects.filter(parent__isnull=True).all()
    else:
        folders = Folder.objects.filter(parent=parent).all()
    for folder in folders:
        size = folder.calculate_total_size

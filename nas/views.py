from typing import Any

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from .serializers import FolderSerializer, \
    FileSerializer, UserSerializer, FolderBasicSerializer, DocumentSerializer, \
    DocumentAbstractSerializer
from .models import Folder, File, Document
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics
import psutil
from django.conf import settings
import os
import sys
import zipfile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import filters


# from .documents import DocDocument


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


@method_decorator(csrf_exempt, name='dispatch')
class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def list(self, request, *args, **kwargs):
        # Get root
        obj = Folder.objects.filter(parent__isnull=True).all()
        obj2 = File.objects.filter(parent__isnull=True).all()
        obj3 = Document.objects.filter(parent__isnull=True).all()

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


@method_decorator(csrf_exempt, name='dispatch')
class FileViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    queryset = File.objects.all()
    serializer_class = FileSerializer
    search_fields = ['file']

    # def get_queryset(self):
    #     queryset = File.objects.all()
    #     search = self.request.query_params.get("search")
    #     if search:
    #         docs = FileDocument.search().query("match", file=search).to_queryset()
    #         queryset = docs
    #         # queryset = NewsFeed.objects.filter(
    #         #     content__fts=search).order_by("-posted_time")
    #
    #     return queryset


@method_decorator(csrf_exempt, name='dispatch')
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    search_fields = ['content']

    # def get_queryset(self):
    #     queryset = Document.objects.all()
    #     search = self.request.query_params.get("search")
    #     if search:
    #         docs = DocDocument.search().query("match", content=search).to_queryset()
    #         queryset = docs
    #
    #     return queryset


@method_decorator(csrf_exempt, name='dispatch')
class SystemInfoView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        cpu = psutil.cpu_percent()
        disk = psutil.disk_usage("/")
        if sys.platform.startswith('linux'):
            disk = psutil.disk_usage(os.getcwd())
        memory = psutil.virtual_memory()
        data = {
            "cpu": cpu,
            "disk": {"used": disk.used, "total": disk.total},
            "memory": {"used": memory.used, "total": memory.total}
        }
        try:
            from coral.enviro.board import EnviroBoard
            enviro = EnviroBoard()
            data['temperature'] = enviro.temperature
            data['humidity'] = enviro.humidity
            data['pressure'] = enviro.pressure
        except Exception as e:
            pass

        return Response(data=data)


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


@csrf_exempt
def download(request, folder):
    if request.method == "POST":
        return JsonResponse(
            data={"download_url": request.build_absolute_uri(reverse("download", kwargs={"folder": folder}))})
    """Download archive zip file of code snippets"""
    # response = HttpResponse(content_type='application/zip')
    response = HttpResponse(content_type='application/zip')
    zf = zipfile.ZipFile(response, 'w')
    folder = Folder.objects.get(id=folder)
    files = File.objects.filter(parent=folder).all()

    for file in files:
        with open(file.file.path, 'rb') as f:
            zf.writestr(file.file.name, f.read())

    zipfile_name = f"{folder.name}.zip"

    # return as zipfile
    response['Content-Disposition'] = f'attachment; filename={zipfile_name}'
    return response


@csrf_exempt
def upload(request, file_index):
    from .key import aws_settings
    import boto3

    s3_client = boto3.client('s3', aws_access_key_id=aws_settings['access_id'],
                             aws_secret_access_key=aws_settings['access_key'])
    file = File.objects.filter(id=file_index).first()
    if file:
        try:
            p = file.parent
            path = os.path.basename(file.file.name)
            depth = 0
            while p:
                path = os.path.join(p.name, path)
                p = p.parent
                depth += 1
            if depth > 400:
                return JsonResponse(data={"message": "Too many folder"}, status=500)
            response = s3_client.upload_file(file.file.path, aws_settings['bucket_name'], path)
            file.has_uploaded_to_cloud = True
            file.save()
        except Exception as e:
            return JsonResponse(data={"message": str(e)}, status=500)
    else:
        return JsonResponse(status=404, data={"message": "file not found"})
    return JsonResponse(data={"status": "Ok"}, status=201)

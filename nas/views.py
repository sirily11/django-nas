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

        disk = psutil.disk_usage("/")
        if sys.platform.startswith('linux'):
            disk = psutil.disk_usage(os.getcwd())
        # total_size = sum(o.total_size for o in obj)
        # total_size += sum(o.size for o in obj2 if o.size)

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
                "total_size": disk.used
            },
                status=200)
        except Exception:
            return Response(status=500)


@method_decorator(csrf_exempt, name='dispatch')
class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


@method_decorator(csrf_exempt, name='dispatch')
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


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

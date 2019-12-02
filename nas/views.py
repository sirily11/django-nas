from django.shortcuts import render, HttpResponse
from .serializers import FolderSerializer, FileSerializer, UserSerializer, FolderBasicSerializer
from .models import Folder, File
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import psutil
import json
import os


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


# Create your views here.
class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def list(self, request, *args, **kwargs):
        # Get root
        obj = Folder.objects.filter(parent__isnull=True).all()
        obj2 = File.objects.filter(parent__isnull=True).all()

        serializer = FolderBasicSerializer(obj, many=True)
        serializer2 = FileSerializer(obj2, many=True)

        try:

            return Response(data={
                "name": "root",
                "folders": serializer.data,
                "files": serializer2.data
            },
                status=200)
        except Exception:
            return Response(status=500)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


def index(request):
    files = File.objects.filter(parent__isnull=True).all()
    folders = Folder.objects.filter(parent__isnull=True).all()
    size = round(sum(f.size for f in files if f.size) / 1024 / 1024, 2)
    space = f"{round(psutil.disk_usage('/').used / 1024 / 1024, 2)} MB/" \
        f"{round(psutil.disk_usage('/').total / 1024 / 1024, 2)} MB"
    context = {"files": files, "folders": folders, "size": size, "space": space}
    return render(request, 'nas/index.html', context=context)


def detail(request, pk):
    folder = Folder.objects.get(pk=pk)
    files = File.objects.filter(parent=folder).all()
    folders = Folder.objects.filter(parent=folder).all()
    p = folder
    menus = []
    while p:
        menus.append({"name": p.name, "id": p.id})
        p = p.parent

    menus.reverse()
    size = round(sum(f.size for f in files if f.size) / 1024 / 1024, 2)
    space = f"{round(psutil.disk_usage('/').used / 1024 / 1024, 2)} MB/" \
        f"{round(psutil.disk_usage('/').total / 1024 / 1024, 2)} MB"
    context = {"files": files, "folders": folders, 'menus': menus, "size": size, "space": space, "current_dir": pk}
    return render(request, 'nas/index.html', context=context)


@csrf_exempt
def upload(request):
    if request.method == "POST":
        file = request.FILES['files']
        current_dir = request.POST.get('current_dir')
        parent = None
        if current_dir:
            # not root
            parent = Folder.objects.get(pk=current_dir)

        File.objects.create(file=file, owner=request.user, parent=parent)
        return HttpResponse(content=json.dumps({"status": "ok"}))



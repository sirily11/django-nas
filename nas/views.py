from django.shortcuts import render
from .serializers import FolderSerializer, FileSerializer, UserSerializer
from .models import Folder, File
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


# Create your views here.
class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def list(self, request, *args, **kwargs):
        obj = Folder.objects.filter(parent__isnull=True).all()
        serializer = FolderSerializer(obj, many=True)
        try:
            return Response(data=serializer.data, status=200)
        except Exception:
            return Response(status=500)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

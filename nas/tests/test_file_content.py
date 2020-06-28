import json
import shutil
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from nas.models import File as FileObj, MusicMetaData, Folder, File
from nas.tests.const_params import TEST_DIR
from nas.utils.utils import get_mp3_metadata, get_mp4_metadata
from nas.views import MusicView, AlbumView, ArtistView, FileContentView
from django.test import override_settings


class FileTest(TestCase):

    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except Exception as e:
            print(e)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_create_file_content(self):
        factory = APIRequestFactory()
        view = FileContentView.as_view({'post': 'create'})
        request = factory.post('/files/', {
            "filename": "Test",
            "file_content": "Hello"
        })
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(File.objects.count(), 1)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_get_file_content(self):
        file = FileObj.objects.create(file=SimpleUploadedFile(name="c", content=b'abc'))

        factory = APIRequestFactory()
        view = FileContentView.as_view({'get': 'retrieve'})
        request = factory.get('/files/')
        response = view(request, pk=file.pk)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['file_content'], 'abc')

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_update_file_content(self):
        file = FileObj.objects.create(file=SimpleUploadedFile(name="c", content=b'test'))
        factory = APIRequestFactory()

        view = FileContentView.as_view({'patch': 'update'})
        request = factory.patch('/files/', {
            "file_content": "Hello"
        })
        response = view(request, pk=file.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['file_content'], 'Hello')

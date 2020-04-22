import json
import shutil
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from nas.models import File as FileObj, MusicMetaData, Folder
from nas.tests.const_params import TEST_DIR
from nas.utils.utils import get_mp3_metadata, get_mp4_metadata
from nas.views import MusicView, AlbumView, ArtistView
from django.test import override_settings


class FileTest(TestCase):

    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except Exception as e:
            print(e)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_get_file_relative_filename(self):
        folder_a = Folder.objects.create(name="a")
        folder_a_b = Folder.objects.create(name="b", parent=folder_a)
        file = FileObj.objects.create(file=SimpleUploadedFile(name="c", content=b'abc'), parent=folder_a_b)
        self.assertEqual(file.relative_filename(folder_a.id), "b/c")

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_get_file_relative_filename(self):
        folder_a = Folder.objects.create(name="a")
        folder_a_b = Folder.objects.create(name="b", parent=folder_a)
        file = FileObj.objects.create(file=SimpleUploadedFile(name="c", content=b'abc'), parent=folder_a_b)
        self.assertEqual(file.relative_filename(None), "a/b/c")

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_download_multiple_files(self):
        file = FileObj.objects.create(file=SimpleUploadedFile(name="a", content=b'abc'))
        file2 = FileObj.objects.create(file=SimpleUploadedFile(name="b", content=b'abc'))
        file3 = FileObj.objects.create(file=SimpleUploadedFile(name="c", content=b'abc'))
        url = reverse("download_multiple_files")
        response = self.client.post(url, json.dumps([file.id, file2.id, file3.id]))
        self.assertEqual(response.status_code, 201)

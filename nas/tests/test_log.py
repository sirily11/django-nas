import shutil
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from nas.models import File as FileObj, MusicMetaData, Document, BookCollection, Logs
from nas.tests.const_params import TEST_DIR
from nas.views import DocumentViewSet, BookCollectionViewSet, MusicView
from django.test import override_settings


class LogTest(TestCase):

    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except Exception as e:
            print(e)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_create_collection(self):
        """
        Create document and set collection
        :return:
        """
        factory = APIRequestFactory()
        view = MusicView.as_view()
        request = factory.patch('/music-metadata')
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Logs.objects.count(), 1)


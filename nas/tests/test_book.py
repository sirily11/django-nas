import shutil
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from nas.models import File as FileObj, MusicMetaData, Document, BookCollection
from nas.tests.const_params import TEST_DIR
from nas.views import DocumentViewSet, BookCollectionViewSet
from django.test import override_settings


class MusicMetaDataTest(TestCase):

    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except Exception as e:
            print(e)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_set_collection(self):
        """
        Create document and set collection
        :return:
        """
        collection = BookCollection.objects.create(name="My Collection")

        factory = APIRequestFactory()
        view = DocumentViewSet.as_view({"post": "create"})
        request = factory.post('/document', data={"name": "document1", "collection": collection.id})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "document1")
        self.assertEqual(response.data['collection'], collection.id)
        self.assertEqual(response.data['book_collection']['name'], "My Collection")

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_create_collection(self):
        """
        Create document and set collection
        :return:
        """
        factory = APIRequestFactory()
        view = BookCollectionViewSet.as_view({"post": "create"})
        request = factory.post('/collection', data={"name": "collection"})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "collection")

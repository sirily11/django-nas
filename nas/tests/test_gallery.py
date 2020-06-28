import shutil

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from nas.models import File, ImageMetaData
from nas.tests.const_params import TEST_DIR
from nas.views import ImageGalleryView


class TestGallery(TestCase):
    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except Exception as e:
            print(e)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_list_images(self):
        """
        Create document and set collection
        :return:
        """
        with open('/test-files/test_image.jpg', 'rb') as f:
            upload_file = SimpleUploadedFile('test_image.jpg', f.read())
            File.objects.create(file=upload_file)
            File.objects.create(file=upload_file)

        factory = APIRequestFactory()
        view = ImageGalleryView.as_view({"get": "list"})
        request = factory.get('/gallery')
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data['results']), 2)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_list_images2(self):
        """
        Create document and set collection
        :return:
        """
        with open('/test-files/test_image.jpg', 'rb') as f:
            upload_file = SimpleUploadedFile('test_image.jpg', f.read())
            File.objects.create(file=upload_file)
            File.objects.create(file=upload_file)

        File.objects.create(file=SimpleUploadedFile('test_file.txt', b'hello'))

        factory = APIRequestFactory()
        view = ImageGalleryView.as_view({"get": "list"})
        request = factory.get('/gallery')
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data['results']), 2)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_update_image_metadata(self):
        """
        Create document and set collection
        :return:
        """
        with open('/test-files/test_image.jpg', 'rb') as f:
            upload_file = SimpleUploadedFile('test_image.jpg', f.read())
            File.objects.create(file=upload_file)
            File.objects.create(file=upload_file)

        File.objects.create(file=SimpleUploadedFile('test_file.txt', b'hello'))

        factory = APIRequestFactory()
        view = ImageGalleryView.as_view({"patch": "update"})
        request = factory.patch('/gallery')
        response = view(request, pk=2)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(ImageMetaData.objects.count(), 2)

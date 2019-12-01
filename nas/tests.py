from django.test import TestCase
from .models import Folder, File as FileObj
from django.contrib.auth.models import User
from os.path import join
from os import remove
from django.core.files import File
import mock


# Create your tests here.
class BaseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="abc@abc.com", password="abc")
        self.base = Folder.objects.create(name="Base", owner=self.user, description="Some")

    def test_add_file(self):
        moc_file: File = mock.MagicMock(spec=File)
        moc_file.name = "Test1"
        file = FileObj.objects.create(file=moc_file, parent=self.base, owner=self.user)
        self.assertTrue(join("Base", "Test1") in file.file.path)

    def tearDown(self):
        remove("django_nas")


class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="abc@abc.com", password="abc")
        # root folder
        self.video = Folder.objects.create(name="VideoTest", owner=self.user)
        self.images = Folder.objects.create(name='ImagesTest', owner=self.user)
        moc_file: File = mock.MagicMock(spec=File)
        moc_file.name = "Test1"
        self.file = FileObj.objects.create(file=moc_file, owner=self.user)

    def tearDown(self):
        self.video.delete()
        self.images.delete()

    def test_list(self):

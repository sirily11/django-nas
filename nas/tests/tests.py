from django.test import TestCase
from rest_framework.test import APIRequestFactory
from nas.utils.utils import get_list_files, create_folders, has_parent, \
    get_mp4_metadata, get_mp3_metadata
from nas.utils.utils2 import is_video, is_audio
from nas.views import FolderViewSet, FileViewSet, MusicView, AlbumView, ArtistView
from nas.models import Folder, File as FileObj, MusicMetaData
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
import mock


class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="abc@abc.com", password="abc")
        # root folder
        self.video = Folder.objects.create(name="VideoTest", owner=self.user)
        self.images = Folder.objects.create(name='ImagesTest', owner=self.user)
        moc_file: File = mock.MagicMock(spec=File)
        moc_file.name = "Test1"
        moc_file.size = 10
        self.file = FileObj.objects.create(file=moc_file, owner=self.user)

    # def tearDown(self):
    #     try:
    #         p = join(os.getcwd(), "django_nas/media/")
    #         remove(join(p, 'Test1'))
    #         remove(join(p, "VideoTest/Test1"))
    #         os.removedirs(join(p, "VideoTest"))
    #     except Exception:
    #         pass

    def test_list(self):
        factory = APIRequestFactory()
        view = FolderViewSet.as_view({'get': 'list'})
        request = factory.get("/folder/")
        response = view(request)
        self.assertEqual(len(response.data['files']), 1)
        self.assertEqual(len(response.data['folders']), 2)
        self.assertEqual(response.data['folders'][0]['name'], 'VideoTest')
        self.assertEqual(response.data['folders'][1]['name'], 'ImagesTest')

    def test_inner_files(self):
        moc_file: File = mock.MagicMock(spec=File)
        moc_file.name = "Test1"
        moc_file.size = 10
        self.video_file = FileObj.objects.create(file=moc_file, owner=self.user, parent=self.video)
        factory = APIRequestFactory()
        view = FolderViewSet.as_view({'get': 'retrieve'})
        request = factory.get(f"/folder/")
        response = view(request, pk=self.video.pk)
        self.assertEqual(len(response.data['files']), 1)

    def test_inner_folders(self):
        folder1 = Folder.objects.create(name="a", owner=self.user, parent=self.video)
        folder2 = Folder.objects.create(name="b", owner=self.user, parent=self.video)
        factory = APIRequestFactory()
        view = FolderViewSet.as_view({'get': 'list'})
        request = factory.get("/folder/")
        response = view(request)
        self.assertEqual(len(response.data['folders']), 2)
        view = FolderViewSet.as_view({'get': 'retrieve'})
        request = factory.get("/folder/")
        response = view(request, pk=self.video.pk)
        self.assertEqual(len(response.data['folders']), 2)


class SizeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="abc@abc.com", password="abc")
        self.base = Folder.objects.create(name="Base", owner=self.user, description="Some")
        self.sub_folder = Folder.objects.create(name="sub_a", parent=self.base)

    def tearDown(self):
        self.sub_folder.delete()
        self.base.delete()

    def test(self):
        self.assertEqual(self.base.total_size, 0)
        self.assertEqual(self.base.total_size, 0)

    # def test_add_file(self):
    #     moc_file: File = mock.MagicMock(spec=File)
    #     moc_file.name = "Test1"
    #     moc_file.size = 30
    #
    #     moc_file2: File = mock.MagicMock(spec=File)
    #     moc_file2.name = "Test2"
    #     moc_file2.size = 40
    #
    #     moc_file3: File = mock.MagicMock(spec=File)
    #     moc_file3.name = "Test2"
    #     moc_file3.size = 40
    #
    #     FileObj(file=moc_file, parent=self.base, owner=self.user)
    #     self.assertEqual(self.base.total_size, 30)
    #
    #     FileObj(file=moc_file2, parent=self.base, owner=self.user)
    #     self.assertEqual(self.base.total_size, 70)
    #
    #     FileObj.objects.create(file=moc_file3, parent=self.sub_folder)
    #     self.assertEqual(self.sub_folder.total_size, 40)
    #     self.assertEqual(self.base.total_size, 100)


from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import force_authenticate, APIRequestFactory

from nas.utils import get_list_files, create_folders, has_parent, \
    get_mp4_metadata, get_mp3_metadata, get_and_create_music_metadata
from .utils2 import is_video, is_audio
from .views import FolderViewSet, FileViewSet
from .models import Folder, File as FileObj, MusicMetaData
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
import mock
import os


# Create your tests here.
# class BaseTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(email="abc@abc.com", password="abc")
#         self.base = Folder.objects.create(name="Base", owner=self.user, description="Some")
#
#     def test_add_file(self):
#         moc_file: File = mock.MagicMock(spec=File)
#         moc_file.name = "Test1"
#         file = FileObj.objects.create(file=moc_file, parent=self.base, owner=self.user)
#         self.assertTrue(join("Base", "Test1") in file.file.path)
#
#     # def tearDown(self):
#     #     remove(join(os.getcwd(), "django_nas/media/Base/Test1"))
#     #     os.removedirs(join(os.getcwd(), "django_nas/media/Base/"))


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


class GetFilesByFolderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="abc@abc.com", password="abc")
        self.base = Folder.objects.create(name="Base", owner=self.user, description="Some")
        self.sub_folder = Folder.objects.create(name="sub_a", parent=self.base)
        self.sub_folder2 = Folder.objects.create(name="sub_b", parent=self.base)
        self.sub_sub_folder = Folder.objects.create(name="sub_sub_a", parent=self.sub_folder)
        self.sub_sub_folder2 = Folder.objects.create(name="sub_sub_a", parent=self.sub_folder2)

    def test_basic(self):
        """
        Basic test without sub folder
        :return:
        """
        [FileObj.objects.create(parent=self.base) for i in range(10)]
        files = get_list_files(self.base)
        self.assertEqual(len(files), 10)

    def test_sub_folder(self):
        """
        Test with two sub-folders
        :return:
        """
        [FileObj.objects.create(parent=self.base) for i in range(10)]
        [FileObj.objects.create(parent=self.sub_folder) for i in range(10)]
        [FileObj.objects.create(parent=self.sub_folder2) for i in range(10)]
        files = get_list_files(self.base)
        self.assertEqual(len(files), 30)

    def test_sub_sub_folder(self):
        """
        Test with two sub-folders
        And one sub folder has one sub-sub-folder
        :return:
        """
        [FileObj.objects.create(parent=self.base) for i in range(10)]
        [FileObj.objects.create(parent=self.sub_folder) for i in range(10)]
        [FileObj.objects.create(parent=self.sub_folder2) for i in range(10)]
        [FileObj.objects.create(parent=self.sub_sub_folder) for i in range(10)]
        [FileObj.objects.create(parent=self.sub_sub_folder2) for i in range(10)]
        files = get_list_files(self.base)
        self.assertEqual(len(files), 50)


class FolderUploadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="abc@abc.com", password="abc")

    def test_has_parent(self):
        path = "a/b/c.txt"
        has = has_parent(path)
        self.assertTrue(has)

    def test_has_parent2(self):
        path = "c.txt"
        has = has_parent(path)
        self.assertFalse(has)

    def test_create_folders(self):
        """
        Creat list of folders in root
        :return:
        """
        base, folder = create_folders(["a", "b", "c.txt"], None)
        self.assertEqual(base, "c.txt")
        self.assertEqual(folder.name, "b")
        self.assertEqual(folder.parent.name, "a")
        self.assertEqual(folder.parent.parent, None)

    def test_create_folders2(self):
        """
        Create list of folders where some of the folder already exist
        :return:
        """
        a = Folder.objects.create(name="a")
        base, folder = create_folders(["a", "b", "c.txt"], None)
        self.assertEqual(base, "c.txt")
        self.assertEqual(folder.name, "b")
        self.assertEqual(folder.parent, a)
        self.assertEqual(folder.parent.parent, None)

    def test_create_folders2_2(self):
        """
        Create list of folders where some of the folder already exist
        :return:
        """
        a = Folder.objects.create(name="a")
        b = Folder.objects.create(name="b", parent=a)
        base, folder = create_folders(["a", "b", "c.txt"], None)
        self.assertEqual(base, "c.txt")
        self.assertEqual(folder, b)
        self.assertEqual(folder.parent, a)
        self.assertEqual(folder.parent.parent, None)

    def test_create_folders2_3(self):
        """
        Create list of folders where some of the folder already exist
        :return:
        """
        a = Folder.objects.create(name="a")
        b = Folder.objects.create(name="b", parent=a)
        base, folder = create_folders(["a", "b", "c.txt"], None)
        base, folder = create_folders(['a', 'b', 'c.txt'], a)
        self.assertEqual(Folder.objects.filter(name='a').count(), 2)
        self.assertEqual(Folder.objects.filter(parent=a).count(), 2)

    def test_create_folders3(self):
        """
        Create list of folders where base has folders but doesn't match
        :return:
        """
        a = Folder.objects.create(name="a")
        b = Folder.objects.create(name="b")
        base, folder = create_folders(["c", "b", "c.txt"], None)
        self.assertEqual(base, "c.txt")
        self.assertEqual(folder.name, "b")
        self.assertEqual(folder.parent.name, "c")
        self.assertEqual(folder.parent.parent, None)

    def test_upload(self):
        factory = APIRequestFactory()
        view = FileViewSet.as_view({'post': 'create'})
        file = SimpleUploadedFile("a/file.mp4", b"file_content", content_type="video/mp4")
        request = factory.post('/files/', {"file": file, "paths": "a/file.mp4"})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Folder.objects.filter(name='a').exists())

    def test_upload2(self):
        factory = APIRequestFactory()
        view = FileViewSet.as_view({'post': 'create'})
        file = SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")
        request = factory.post('/files/', {"file": file, "paths": "a/b/file.mp4"})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Folder.objects.filter(name='a').all()), 1)
        self.assertEqual(len(Folder.objects.filter(name='b').all()), 1)

    def test_upload3(self):
        factory = APIRequestFactory()
        view = FileViewSet.as_view({'post': 'create'})
        file = SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")
        file2 = SimpleUploadedFile("file2.mp4", b"file_content", content_type="video/mp4")
        request = factory.post('/files/', {"file": file, "paths": "a/file.mp4"})
        response = view(request)
        self.assertEqual(Folder.objects.filter(name='a').count(), 1)
        a = Folder.objects.filter(name='a').first()
        request = factory.post('/files/', {"file": file2, "paths": "a/file2.mp4", "parent": a.id})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Folder.objects.filter(name='a').count(), 2)
        self.assertEqual(Folder.objects.filter(parent=a).count(), 1)


class UtilTest(TestCase):
    def test_is_video(self):
        p = "a.avi"
        self.assertTrue(is_video(p))

    def test_is_audio(self):
        p = 'a.m4a'
        self.assertTrue(is_audio(p))


class MusicMetaDataTest(TestCase):
    def test_m4a_audio(self):
        title, album, artist, year, genre, cover, duration = get_mp4_metadata("/test-music/test.m4a")
        self.assertEqual(title, "Carry On")
        self.assertEqual(album, 'Carry On (From the Original Motion Picture "Detective Pikachu") - Single')
        self.assertTrue("2019" in year)
        self.assertTrue(cover.size > 0)

    def test_mp3_audio(self):
        title, album, artist, year, genre, cover, duration = get_mp3_metadata("/test-music/test.mp3")
        self.assertEqual(year, "2019")
        self.assertTrue(cover.size > 0)

    def test_get_and_create(self):
        with open('/test-music/test.mp3', 'rb') as f:
            nas_file = FileObj.objects.create(file=SimpleUploadedFile('test.mp3', f.read()))
            nas_file.save()
            print(nas_file.id)

            get_and_create_music_metadata(nas_file)
            meta = MusicMetaData.objects.filter(file=nas_file).first()

            self.assertTrue(meta is not None)
            self.assertEqual(meta.title, "きみと恋のままで終われない いつも夢のままじゃいられない")
            self.assertTrue(meta.picture is not None)

    def test_get_and_create2(self):
        with open('/test-music/test.m4a', 'rb') as f:
            nas_file = FileObj.objects.create(file=SimpleUploadedFile('test.m4a', f.read()))
            nas_file.save()
            print(nas_file.id)

            get_and_create_music_metadata(nas_file)
            meta = MusicMetaData.objects.filter(file=nas_file).first()

            self.assertTrue(meta is not None)
            self.assertEqual(meta.title, "Carry On")
            self.assertTrue(meta.picture is not None)

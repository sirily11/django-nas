import shutil

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from nas.models import Folder, File as FileObj, File
from nas.tests.const_params import TEST_DIR
from nas.utils.utils import get_list_files, create_folders, has_parent, extra_text_from_current_files
from nas.utils.utils2 import is_video, is_audio
from nas.views import FileViewSet
from django.test import override_settings


class GetFilesByFolderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="abc@abc.com", password="abc")
        self.base = Folder.objects.create(name="Base", owner=self.user, description="Some")
        self.sub_folder = Folder.objects.create(name="sub_a", parent=self.base)
        self.sub_folder2 = Folder.objects.create(name="sub_b", parent=self.base)
        self.sub_sub_folder = Folder.objects.create(name="sub_sub_a", parent=self.sub_folder)
        self.sub_sub_folder2 = Folder.objects.create(name="sub_sub_a", parent=self.sub_folder2)

    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except Exception as e:
            print(e)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_basic(self):
        """
        Basic test without sub folder
        :return:
        """
        [FileObj.objects.create(parent=self.base) for i in range(10)]
        files = get_list_files(self.base)
        self.assertEqual(len(files), 10)

    @override_settings(MEDIA_ROOT=TEST_DIR)
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

    @override_settings(MEDIA_ROOT=TEST_DIR)
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

    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except Exception as e:
            print(e)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_has_parent(self):
        path = "a/b/c.txt"
        has = has_parent(path)
        self.assertTrue(has)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_has_parent2(self):
        path = "c.txt"
        has = has_parent(path)
        self.assertFalse(has)

    @override_settings(MEDIA_ROOT=TEST_DIR)
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

    @override_settings(MEDIA_ROOT=TEST_DIR)
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

    @override_settings(MEDIA_ROOT=TEST_DIR)
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

    @override_settings(MEDIA_ROOT=TEST_DIR)
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

    @override_settings(MEDIA_ROOT=TEST_DIR)
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

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_upload(self):
        factory = APIRequestFactory()
        view = FileViewSet.as_view({'post': 'create'})
        file = SimpleUploadedFile("a/file.mp4", b"file_content", content_type="video/mp4")
        request = factory.post('/files/', {"file": file, "paths": "a/file.mp4"})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Folder.objects.filter(name='a').exists())

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_upload2(self):
        factory = APIRequestFactory()
        view = FileViewSet.as_view({'post': 'create'})
        file = SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")
        request = factory.post('/files/', {"file": file, "paths": "a/b/file.mp4"})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Folder.objects.filter(name='a').all()), 1)
        self.assertEqual(len(Folder.objects.filter(name='b').all()), 1)

    @override_settings(MEDIA_ROOT=TEST_DIR)
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
    def setUp(self) -> None:
        with open('/test-files/test.mp3', 'rb') as f:
            self.upload = SimpleUploadedFile('test.mp3', f.read())

        with open('/test-files/test.m4a', 'rb') as f:
            self.upload2 = SimpleUploadedFile('test.m4a', f.read())

        with open('/test-files/test.pdf', 'rb') as f:
            self.upload3 = SimpleUploadedFile('test.pdf', f.read())

        with open('/test-files/testfile.txt', 'rb') as f:
            self.upload4 = SimpleUploadedFile('testfile.txt', f.read())

        with open('/test-files/testfile2.txt', 'rb') as f:
            self.upload5 = SimpleUploadedFile('testfile2.txt', f.read())

    def test_is_video(self):
        p = "a.avi"
        self.assertTrue(is_video(p))

    def test_is_audio(self):
        p = 'a.m4a'
        self.assertTrue(is_audio(p))

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_file_text_extra(self):
        file3 = FileObj.objects.create(file=self.upload3)
        file4 = FileObj.objects.create(file=self.upload4)
        file5 = FileObj.objects.create(file=self.upload5)

        self.assertTrue(file3.description is not None)
        self.assertTrue(file4.description is not None)
        self.assertTrue(file5.description is not None)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_file_text_extra2(self):
        file1 = FileObj.objects.create(file=self.upload)
        file2 = FileObj.objects.create(file=self.upload2)
        file3 = FileObj.objects.create(file=self.upload3)
        file4 = FileObj.objects.create(file=self.upload4)
        file5 = FileObj.objects.create(file=self.upload5)

        num = extra_text_from_current_files()
        self.assertEqual(num, 3)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_file_text_extra_api(self):
        file1 = FileObj.objects.create(file=self.upload)
        file2 = FileObj.objects.create(file=self.upload2)
        file3 = FileObj.objects.create(file=self.upload3)
        file4 = FileObj.objects.create(file=self.upload4)
        file5 = FileObj.objects.create(file=self.upload5)

        num = extra_text_from_current_files()
        res = self.client.post('/api/update_file_description')
        self.assertEqual(res.json()['number_updates'], 3)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_file_search(self):
        factory = APIRequestFactory()
        file1 = FileObj.objects.create(file=self.upload)
        file2 = FileObj.objects.create(file=self.upload2)
        file3 = FileObj.objects.create(file=self.upload3)
        file4 = FileObj.objects.create(file=self.upload4)
        file5 = FileObj.objects.create(file=self.upload5)
        req = factory.get('/api/file?search=cnn', )
        view = FileViewSet.as_view({'get': 'list'})
        res = view(req)
        self.assertEqual(len(res.data), 2)

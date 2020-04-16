import shutil
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from nas.models import File as FileObj, MusicMetaData
from nas.tests.const_params import TEST_DIR
from nas.utils.utils import get_mp3_metadata, get_mp4_metadata
from nas.views import MusicView, AlbumView, ArtistView
from django.test import override_settings


class MusicMetaDataTest(TestCase):

    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except Exception as e:
            print(e)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_m4a_audio(self):
        title, album, artist, year, genre, cover, duration, album_artist, track = \
            get_mp4_metadata("/test-music/test.m4a")
        self.assertEqual(title, "Carry On")
        self.assertEqual(album, 'Carry On (From the Original Motion Picture "Detective Pikachu") - Single')
        self.assertTrue("2019" in year)
        self.assertTrue(cover.size > 0)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_mp3_audio(self):
        title, album, artist, year, genre, cover, duration, album_artist, track = get_mp3_metadata(
            "/test-music/test.mp3")
        self.assertEqual(year, "2019")
        self.assertTrue(cover.size > 0)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_get_and_create(self):
        with open('/test-music/test.mp3', 'rb') as f:
            nas_file = FileObj.objects.create(file=SimpleUploadedFile('test.mp3', f.read()))
            meta = MusicMetaData.objects.filter(file=nas_file).first()
            self.assertTrue(meta is not None)
            self.assertEqual(meta.title, "きみと恋のままで終われない いつも夢のままじゃいられない")
            self.assertTrue(meta.picture is not None)
            self.assertEqual(meta.track, 1)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_get_and_create2(self):
        with open('/test-music/test.m4a', 'rb') as f:
            nas_file = FileObj.objects.create(file=SimpleUploadedFile('test.m4a', f.read()))
            meta = MusicMetaData.objects.filter(file=nas_file).first()
            self.assertTrue(meta is not None)
            self.assertEqual(meta.title, "Carry On")
            self.assertEqual(meta.track, 1)
            self.assertTrue(meta.picture is not None)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_get_and_create3(self):
        with open('/test-music/test2.mp3', 'rb') as f:
            nas_file = FileObj.objects.create(file=SimpleUploadedFile('test2.mp3', f.read()))
            meta = MusicMetaData.objects.filter(file=nas_file).first()
            self.assertTrue(meta is not None)
            self.assertEqual(meta.title, "Unlasting")
            self.assertEqual(meta.track, 1)
            self.assertTrue(meta.picture is not None)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_update_metadata(self):
        """
        Update existing music file
        :return:
        """

        with open('/test-music/test.mp3', 'rb') as f:
            nas_file = FileObj.objects.create(file=SimpleUploadedFile('test.mp3', f.read()))
            data: MusicMetaData = MusicMetaData.objects.filter(file=nas_file).first()
            data.delete()

        with open('/test-music/test.m4a', 'rb') as f:
            nas_file = FileObj.objects.create(file=SimpleUploadedFile('test.m4a', f.read()))
            data: MusicMetaData = MusicMetaData.objects.filter(file=nas_file).first()
            data.delete()

        factory = APIRequestFactory()
        view = MusicView.as_view()
        request = factory.patch('/music/')
        response = view(request)
        meta = MusicMetaData.objects.all()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(meta), 2)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_album_view(self):
        MusicMetaData.objects.create(title='a', album='a')
        MusicMetaData.objects.create(title='a', album='b')
        MusicMetaData.objects.create(title='a', album='c')
        MusicMetaData.objects.create(title='a', album='d')

        factory = APIRequestFactory()
        view = AlbumView.as_view()
        request = factory.get('/album/')
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data[0]['album'], 'a')
        self.assertEqual(response.data[1]['album'], 'b')
        self.assertEqual(response.data[2]['album'], 'c')
        self.assertEqual(response.data[3]['album'], 'd')

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_artist_view(self):
        MusicMetaData.objects.create(title='a', album='a', artist='a')
        MusicMetaData.objects.create(title='a', album='b', artist='b')
        MusicMetaData.objects.create(title='a', album='c', artist='a')
        MusicMetaData.objects.create(title='a', album='d', artist='b')

        factory = APIRequestFactory()
        view = ArtistView.as_view()
        request = factory.get('/artist/')
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_like(self):
        with open('/test-music/test.mp3', 'rb') as f:
            a = FileObj.objects.create(file=SimpleUploadedFile('test.mp3', f.read()))
            data: MusicMetaData = MusicMetaData.objects.filter(file=a).first()
            data.delete()

        with open('/test-music/test.m4a', 'rb') as f:
            b = FileObj.objects.create(file=SimpleUploadedFile('test.m4a', f.read()))
            data: MusicMetaData = MusicMetaData.objects.filter(file=b).first()
            data.delete()

        MusicMetaData.objects.create(title='a', album='a', artist='a', like=True, file=a)
        MusicMetaData.objects.create(title='b', album='a', artist='a', like=False, file=b)

        factory = APIRequestFactory()
        view = MusicView.as_view()
        request = factory.get('/music/?like=true')
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

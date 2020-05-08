from django.urls import include, path, re_path
from rest_framework import routers
from . import views
from . import utility_views

router = routers.DefaultRouter()
router.register(r'file', views.FileViewSet, base_name="files")
router.register(r'folder', views.FolderViewSet, base_name="folders")
router.register(r'user', views.UserViewSet, base_name="users")
router.register(r'document', views.DocumentViewSet, base_name='documents')
router.register(r'music-metadata', views.MusicMetaDataViewSet, base_name="music-metadata")
router.register(r'book-collection', views.BookCollectionViewSet, basename="books")
router.register(r'logs', views.LogsViewSet, basename="logs")

urlpatterns = [
    path('api/', include(router.urls), name='api'),
    path('system/', views.SystemInfoView.as_view()),
    path('api/download/<int:folder>', utility_views.download, name='download'),
    path('api/download_multiple/', utility_views.download_multiple_files, name='download_multiple_files'),
    path('api/convert/caption/<int:file>', utility_views.convert_vtt_caption),
    path('api/music/', views.MusicView.as_view(), name='music'),
    path('api/music/album/', views.AlbumView.as_view(), name='album'),
    path('api/music/artist/', views.ArtistView.as_view(), name='artist'),
    path('', views.index, name='home'),
    path('s3/<int:file_index>', utility_views.upload, name='upload'),
    path('api/update_file_description', utility_views.update_file_description, name='update-file-description')
]

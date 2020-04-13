from django.urls import include, path, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'file', views.FileViewSet, base_name="files")
router.register(r'folder', views.FolderViewSet, base_name="folders")
router.register(r'user', views.UserViewSet, base_name="users")
router.register(r'document', views.DocumentViewSet, base_name='documents')
router.register(r'music-metadata', views.MusicMetaDataViewSet, base_name="music-metadata")

urlpatterns = [
    path('api/', include(router.urls), name='api'),
    path('system/', views.SystemInfoView.as_view()),
    path('api/download/<int:folder>', views.download, name='download'),
    path('api/music/', views.MusicView.as_view(), name='music'),
    path('', views.index, name='home'),
    path('s3/<int:file_index>', views.upload, name='upload')
]

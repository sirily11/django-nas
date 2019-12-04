from django.urls import include, path, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'file', views.FileViewSet, base_name="files")
router.register(r'folder', views.FolderViewSet, base_name="folders")
router.register(r'user', views.UserViewSet,  base_name="users")
router.register(r'document', views.DocumentViewSet, base_name='documents')

urlpatterns = [
    path('api/', include(router.urls), name='api'),
    path('system/', views.SystemInfoView.as_view()),
    path('', views.index, name='home')
]
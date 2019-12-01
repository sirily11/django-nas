from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'file', views.FileViewSet, base_name="files")
router.register(r'folder', views.FolderViewSet, base_name="folders")
router.register(r'user', views.UserViewSet,  base_name="users")


urlpatterns = [
    path('', include(router.urls)),
]
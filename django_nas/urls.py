from django.urls import path, include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('admin/', admin.site.urls),
path('django-rq/', include('django_rq.urls')),
path('', include("nas.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

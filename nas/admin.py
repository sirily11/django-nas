from django.contrib import admin
from .models import File, Folder, MusicMetaData, Document

# Register your models here.
admin.site.register(File)
admin.site.register(Folder)
admin.site.register(MusicMetaData)
admin.site.register(Document)
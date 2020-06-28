from django.contrib import admin
from .models import File, Folder, MusicMetaData, Document, Logs, BookCollection,ImageMetaData

# Register your models here.
admin.site.register(File)
admin.site.register(Folder)
admin.site.register(MusicMetaData)
admin.site.register(Document)
admin.site.register(Logs)
admin.site.register(BookCollection)
admin.site.register(ImageMetaData)
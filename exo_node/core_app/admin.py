from django.contrib import admin

# Register your models here.
from models import MediaGroup, MediaItem, MediaDownload

admin.site.register(MediaGroup)
admin.site.register(MediaItem)
admin.site.register(MediaDownload)
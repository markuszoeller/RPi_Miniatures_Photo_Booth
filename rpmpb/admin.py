from django.contrib import admin

from .models import Album, Miniature, Tag, PhotoSession

admin.site.register(Album)
admin.site.register(Miniature)
admin.site.register(Tag)
admin.site.register(PhotoSession)

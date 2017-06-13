from django.contrib import admin
from .models import Album, Song, FriendshipStatus

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(FriendshipStatus)
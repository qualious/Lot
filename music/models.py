from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()  # s3

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.album_title + " - " + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)
    song_url = models.CharField(max_length=1000, default="")
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title


class FriendshipStatus(models.Model):
    from_user = models.ForeignKey(User, related_name='friendship_requests_sent')
    to_user = models.ForeignKey(User, related_name='friendship_requests_received')
    friendship_status = models.CharField(max_length=50, default="not_friends")

    def __str__(self):
        if self.friendship_status == "pending":
            return "User #%s has requested friendship to #%s" % (self.from_user.id, self.to_user.id)
        elif self.friendship_status == "friends":
            return "User #%s and #%s are friends" % (self.from_user.id, self.to_user.id)
        else:
            return "User #%s and #%s are not friends" % (self.from_user.id, self.to_user.id)

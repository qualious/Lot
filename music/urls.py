from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    # /music/
    url(r'^$', views.IndexView.as_view(), name='index'), 
    # /music/albums/
    url(r'^albums/$', views.IndexView.as_view(), name='index'),	
    # /register/
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    #/music/albums/'$pk'/
    url(r'^albums/(?P<pk>[0-9]+)/$', views.AlbumDetailView.as_view(), name='detail'),
    #/music/albums/add/
    url(r'^albums/add/$', views.AlbumCreate.as_view(), name='album-add'),
    #/music/albums/'$pk'
    url(r'^albums/(?P<pk>[0-9]+)/update/$', views.AlbumUpdate.as_view(), name='album-update'),
    #/music/albums/'$pk'/delete
    url(r'^albums/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),
    #/music/songs
    url(r'^songs/', views.SongView.as_view(), name='songs'),
    #/music/songs/add/
    url(r'^songs/add/$', views.SongCreate.as_view(), name='song-add'),
    #/music/songs/'$pk'/delete
    url(r'^songs/(?P<pk>[0-9]+)/delete/$', views.SongDelete.as_view(), name='song-delete'),
    #/login/
    url(r'^login/$', views.user_login, name='login'),
    #/logout/
    url(r'^logout/$', views.user_logout, name='logout'),
    #/friends/
    url(r'^friends/$', views.FriendView.as_view(), name='list-friends'),
    #/friends/'$pk'/delete
    url(r'^friends/(?P<pk>[0-9]+)/delete/$', views.friend_remove, name='friend-remove'),
    #/friends/reqs
    url(r'^friends/reqs',  views.FriendshipReqView.as_view(), name='friend-reqs'),
    #/friends/reqs/'$pk'/answer
    url(r'^friends/reqs/accept/(?P<pk>[0-9]+)/$',  views.accept_friend_req, name='accept-friend-req'),
    #/friends/reqs/'$pk'/answer
    url(r'^friends/reqs/decline/(?P<pk>[0-9]+)/$',  views.decline_friend_req, name='decline-friend-req'),
]

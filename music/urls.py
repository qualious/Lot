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
]

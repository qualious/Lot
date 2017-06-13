from django.contrib.auth.models import User
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Album, Song, FriendshipStatus
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm
from django.db import connection


class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()


class SongView(generic.ListView):
    template_name = 'music/songs.html'
    context_object_name = 'songs'

    def get_queryset(self):
        qs = Song.objects.all()
        try:
            if self.request.GET['q'] is not None:
                qs = qs.filter(song_title__icontains=self.request.GET['q'])
            return qs
        except:
            return qs


class AlbumDetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongCreate(CreateView):
    model = Song
    fields = ['album', 'song_title', 'song_url']
    success_url = reverse_lazy('music:index')


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class SongDelete(DeleteView):
    model = Song
    success_url = reverse_lazy('music:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')
        return render(request, self.template_name, {'form': form})


def user_logout(request):
    logout(request)
    return redirect('music:index')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('music:index')
            else:
                return render(request, 'music/login_form.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login_form.html', {'error_message': 'Invalid login, try again!'})
    return render(request, 'music/login_form.html')


class FriendView(generic.ListView):
    template_name = 'music/friends.html'
    context_object_name = 'all_friends'

    def get_queryset(self):
        return FriendshipStatus.objects.all().filter(to_user=self.request.user, friendship_status="friends")


class FriendshipReqView(generic.ListView):
    template_name = 'music/friend_req.html'
    context_object_name = 'friend_reqs'

    def get_queryset(self):
        return FriendshipStatus.objects.all().filter(to_user=self.request.user, friendship_status="pending")


def accept_friend_req(request):
    print('accept')
    from_user = User.objects.all().filter(id=request.POST['user_id'])
    to_user = request.user
    qs = FriendshipStatus.objects.all().filter(from_user=from_user, to_user=request.user, friendship_status="pending")
    qs.delete()
    friendship_status = "friends"
    query = FriendshipStatus(from_user, to_user, friendship_status)
    query.save()
    query2 = FriendshipStatus(to_user, from_user, friendship_status)
    query2.save()
    return redirect('music:friend-reqs')


def decline_friend_req(request):
    print('decline')
    # TODO:  make function for repeated lines
    from_user = User.objects.all().filter(id=request.POST['user_id'])
    to_user = request.user
    qs = FriendshipStatus.objects.all().filter(from_user=from_user, to_user=request.user, friendship_status="pending")
    qs.delete()
    friendship_status = "not_friends"
    query = FriendshipStatus(from_user, to_user, friendship_status)
    query.save()
    return redirect('music:friend-reqs')


def friend_remove(request):
    FriendshipStatus.objects.all().filter(request.user.friendship_status == "not_friends")

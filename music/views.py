from django.contrib.auth.models import User
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Album, Song
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm
from friendship.models import Friend, Follow, FriendshipRequest


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
        return Friend.objects.friends(self.request.user)


class FriendshipReqView(generic.ListView):
    template_name = 'music/friend_req.html'
    context_object_name = 'friend_reqs'

    def get_queryset(self):
        return Friend.objects.unread_requests(user=self.request.user)


def accept_friend_req(request):
    print('accept')
    user1_ID = request.user.id
    user2_ID = User.objects.all().filter(id=request.POST['user_id']).first().id
    friend_request = FriendshipRequest.objects.all().filter(from_user=user2_ID, to_user=user1_ID).first()
    friend_request.accept()
    if Friend.objects.are_friends(user1_ID, user2_ID):
        return redirect("music:list-friends")
    else:
        return render(request, 'music/friends.html', {'error_message': 'Something went wrong, sorry!'})
    # friend_request = FriendshipRequest.objects.get(pk=1)
    # friend_request.accept()
    # return redirect("music:list-friends")
    # other_user = User.objects.get(pk=request.POST['user_id'])
    # new_relationship = Friend.objects.add_friend(request.user, other_user)
    # friend_request = FriendshipRequest.objects.get(pk=request.GET['user_id'])
    # friend_request.accept()
    # return redirect("music:list-friends")


def decline_friend_req(request):
    print('decline')
    user1_ID = request.user.id()
    user2_ID = User.objects.all().filter(id=request.POST['user_id']).first().id
    new_relationship = Friend.objects.add_friend(user1_ID, user2_ID)
    friend_request = FriendshipRequest.objects.all().filter(from_user=user2_ID, to_user=user1_ID).first()
    friend_request.decline()
    if Friend.objects.are_friends(user1_ID, user2_ID):
        return render(request, 'music/friends.html', {'error_message': 'Something went wrong, sorry!'})
    else:
        return redirect("music:list-friends")
    # user1 = request.user
    # user2 = User.objects.all().filter(id=request.POST['user_id'])
    # print('decline')
    # print(request.POST['user_id'])
    # friend_request = FriendshipRequest.objects.get(pk=request.GET['user_id'])
    # friend_request.reject()
    # return redirect("music:list-friends")


def friend_remove(request):
    other_user = User.objects.get(pk=request.POST['q'])
    Friend.objects.remove_friend(request.user, other_user)

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.conf.urls import include
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, ProfileForm, PostForm, LoginForm, UpdateProfile, UpdateProfile2
from django.conf.urls.static import static
from .models import Profile, Image, Comments, UserFollowing
from django.contrib.auth.models import User
from . import models
from annoying.decorators import ajax_request
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# enables sends confirmation mail using @gmail
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def index(request):
    all_images = Image.objects.all()
    all_users = Profile.objects.all()
    all_images = all_images[::-1][:10]
    liker = request.user

    class PostLikes(Image):
        def likes_count(self):
            return self.image_likes.count()
    #next = request.GET.get('next')
    #if next: return redirect(next)
    return render(request, 'main/home.html',  {"all_images": all_images, "all_users":all_users, 'liker': liker})

@login_required(login_url='/login')
def explore(request):
    return render(request, 'main/explore.html')

@login_required(login_url='/login')
def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.imageuploader_profile = request.user
            image.save()
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'main/post.html', {"form": form})

def notification(request):
    return render(request, 'main/notification.html')

# view your own profile
@login_required(login_url='/login')
def account(request):
    usern = request.user.username
    profile = request.user.profile
    obj = get_object_or_404(User, username=usern)
    if request.method == "POST":
        form = UpdateProfile(request.POST)
        form2 = UpdateProfile2(request.POST)
        if form.is_valid():
            form.save()
        if form2.is_valid():
            form.save()
        return redirect('/')
    else:
        form = UpdateProfile(request.POST or None, instance = obj)
        form2 = UpdateProfile2(request.POST or None, instance = obj)
    context = {}
    context['form'] = form
    context['form2'] = form2
    return render(request, 'main/account.html', context)



# view other profiles
@login_required(login_url='/login')
def profile(request, username=None):
    follower = request.user
    followed = User.objects.get(username=username)
    if follower == followed:
        can_follow = False
    else:
        can_follow = True
    try:
        followers = UserFollowing.objects.filter(followed_user=followed).count()
    except:
        followers = 0
    try:
        profile_following = UserFollowing.objects.filter(follower=followed).count()
    except:
        profile_following = 0
    context = {
        'can_follow': can_follow, 'follower': follower, 'followed': followed, 'followers': followers, 'profile_following': profile_following
            }
    try:
        followBool = UserFollowing.objects.get(follower=follower, followed_user=followed)
        if followBool:
            context['following'] = True
    except:
        following = False
        context['following'] = False
    return render(request, 'main/profile.html', context)

def follow_user(request):
    if request.method == 'POST':
        value = request.POST['value']
        follower = request.POST['follower']
        follower = User.objects.get(username=follower)
        followed_user = request.POST['followed_user']
        followed_user = User.objects.get(username=followed_user)
        captured = followed_user.username
        if value == 'follow':
            if follower != followed_user:
                followers_cnt = UserFollowing.objects.create(follower=follower, followed_user=followed_user)
                followers_cnt.save()
        return HttpResponseRedirect(reverse('profile', args=[captured]))
    else:
        return redirect('/')

def unfollow_user(request):
    if request.method == 'POST':
        value = request.POST['value']
        follower = request.POST['follower']
        follower = User.objects.get(username=follower)
        followed_user = request.POST['followed_user']
        followed_user = User.objects.get(username=followed_user)
        captured = followed_user.username
        if value == 'unfollow':
            followers_cnt = UserFollowing.objects.get(follower=follower, followed_user=followed_user)
            followers_cnt.delete()
        return HttpResponseRedirect(reverse('profile', args=[captured]))
    return redirect('/')

def like_post(request):
    if request.method == 'POST':
        liker = request.POST['liker']
        liker = User.objects.get(username=liker)
        post_profile = request.POST['post_profile']
        post_id = request.POST['post_id']
        value = request.POST['value']
        if value == 'like':
            image = Image.objects.get(image_id=post_id)
            image.image_likes.add(liker)
    return redirect('/')

def unlike_post(request):
    if request.method == 'POST':
        liker = request.POST['liker']
        liker = User.objects.get(username=liker)
        post_profile = request.POST['post_profile']
        post_id = request.POST['post_id']
        value = request.POST['value']
        if value == 'unlike':
            image = Image.objects.get(image_id=post_id)
            image.image_likes.remove(liker)
    return redirect('/')

def search(request):
    if request.method == 'POST':
        value = 0
    return redirect('/')

def register(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            userform.save()
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                p = Profile(user=user)
        return redirect('/')
    else:
        userform = UserForm()
    return render(request, "registration/register.html", {"userform":userform})


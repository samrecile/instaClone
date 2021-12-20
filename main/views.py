from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf.urls import include
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, ProfileForm, PostForm, LoginForm
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
    #next = request.GET.get('next')
    #if next: return redirect(next)
    return render(request, 'main/home.html',  {"all_images": all_images, "all_users":all_users})

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
    return render(request, 'main/account.html')

# view other profiles
@login_required(login_url='/login')
def profile(request, prof):
    if request.method == 'POST':
        value = request.POST['value']
        follower = request.POST['follower']
        followed_user = request.POST['followed_user']
        if value == 'follow':
            followers_cnt = UserFollowing.objects.create(follower=follower, followed_user=followed_user)
            followers_cnt.save()
            return redirect('profile/?user='+user)
    else:
        current_user = request.GET.get('user')
        profile = Profile(user=userinst)
        logged_in_user = request.user.username
    return render(request, 'main/profile.html', {'current_user': current_user})


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

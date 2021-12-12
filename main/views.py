from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf.urls import include
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, ProfileForm, PostForm, LoginForm
from django.conf.urls.static import static
from .models import Profile, Image, Comments
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
            form.save()
            image = Image.objects.latest('date')
            image.imageuploader_profile = request.user
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
def profile(request):
    return render(request, 'main/profile.html')


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
                p = Profile(user=userinst)
        return redirect('/')
    else:
        #profileform = ProfileForm()
        userform = UserForm()
    return render(request, "registration/register.html", {"userform":userform})

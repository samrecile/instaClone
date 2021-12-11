from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf.urls import include
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, ProfileForm, PostForm
from django.conf.urls.static import static
from .models import Profile, Image, Comments
from django.contrib.auth.models import User
from . import models
from annoying.decorators import ajax_request

# enables sends confirmation mail using @gmail
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'main/home.html')

def explore(request):
    return render(request, 'main/explore.html')

def post(request):
    return render(request, 'main/post.html')

def notification(request):
    return render(request, 'main/notification.html')

def profile(request):
    return render(request, 'main/userprofile.html')

def logout(request):
    return render(request, 'registration/logout.html')

def login(request):
    return render(request, 'registration/login.html')

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

def upload(request):
    return render(request, 'main/upload.html')
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.conf.urls import include
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import UserForm, ProfileForm, PostForm, LoginForm, UpdateProfile, UpdateProfile2, RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.conf.urls.static import static
from .models import Profile, Image, Comments, UserFollowing
from django.contrib.auth.models import User
from . import models
from annoying.decorators import ajax_request
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib.auth.views import LoginView

# enables sends confirmation mail using @gmail
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def index(request):
    user = request.user 
    followed_user_list = []
    followed_users = UserFollowing.objects.filter(follower=user)
    for followed_user in followed_users:
        followed_user_list.append(followed_user.followed_user)
    all_images = Image.objects.filter(Q(imageuploader_profile__in=followed_user_list) | Q(imageuploader_profile=user))
    all_images = all_images[::-1][:10]
    liker = request.user

    
    return render(request, 'main/home.html',  {"all_images": all_images, 'liker': liker})

@login_required(login_url='/login')
def explore(request):
    yesterday = datetime.today() - timedelta(days=1)
    images = Image.objects.filter(date__gte=yesterday)
    images = images.order_by('image_likes')[:10]
    liker = request.user
    context = {'images': images, 'liker': liker}
    return render(request, 'main/explore.html', context)

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

def delete_post(request, post_id=None):
    if post_id:
        image = Image.objects.get(image_id=post_id)
        captured = request.user.username
        if image.imageuploader_profile == request.user:
            image.delete()
        return HttpResponseRedirect(reverse('profile', args=[captured]))
    else:
        return redirect('/')

   #if request.method == 'POST':
    #    value = request.POST['value']
     #   post_id = request.POST['post_id']
      #  user_profile = request.POST['post_profile']
       # user = User.objects.get(username=user_profile)
    #    captured = user.username
    #    if value == 'unlike':
    #        image = Image.objects.get(image_id=post_id)
    #        image.delete()
    #        return HttpResponseRedirect(reverse('profile', args=[captured]))
    #else:
    #    return redirect('/')


# view your own profile
@login_required(login_url='/login')
def account(request):
    usern = request.user.username
    profile = request.user.profile
    obj = get_object_or_404(User, username=usern)
    obj_prof = obj.profile
    if request.method == "POST":
        form = UpdateProfile(request.POST, instance=request.user)
        form2 = UpdateProfile2(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            
        return redirect('/')
    else:
        form = UpdateProfile(instance=obj)
        form2 = UpdateProfile2(instance=obj_prof)
    context = {}
    context['form'] = form
    context['form2'] = form2
    return render(request, 'main/account.html', context)



# view other profiles and your own
@login_required(login_url='/login')
def profile(request, username=None):
    follower = request.user
    followed = User.objects.get(username=username)
    try:
        followers = UserFollowing.objects.filter(followed_user=followed).count()
    except:
        followers = 0
    try:
        profile_following = UserFollowing.objects.filter(follower=followed).count()
    except:
        profile_following = 0
    context = {
        'follower': follower, 'followed': followed, 'followers': followers, 'profile_following': profile_following
            }
    if follower == followed:
        can_follow = False
        context['can_follow'] = can_follow
        #followers = UserFollowing.objects.filter(followed_user=request.user)
        #following_profile_objects = UserFollowing.objects.filter(follower=request.user)
        #following_profiles = []
        #for obj in following_profile_objects:
        #    x = obj.followed_user
        #    following_profile.append(x)
        #context['followers'] = followers
        #context['following_profiles'] = following_profiles
    else:
        can_follow = True
    try:
        followBool = UserFollowing.objects.get(follower=follower, followed_user=followed)
        if followBool:
            context['following'] = True
    except:
        following = False
        context['following'] = False
    try:
        images = Image.objects.filter(imageuploader_profile=followed)
        context['images'] = images
    except:
        context['images'] = False
    liker = request.user
    context['liker'] = liker
    return render(request, 'main/profile.html', context)

# view you profile followers and the users you follow
@login_required(login_url='/login')
def follower_following(request, username=None):
    if username == request.user.username:
        context = {}
        followers = UserFollowing.objects.filter(followed_user=request.user)
        following_profile_objects = UserFollowing.objects.filter(follower=request.user)
        following_profiles = []
        for obj in following_profile_objects:
            x = obj.followed_user
            following_profile.append(x)
        context['followers'] = followers
        context['following_profiles'] = following_profiles
    else:
        return HttpResponseRedirect(reverse('profile', args=[username]))

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
    context = {}
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]
                user = authenticate(username=username, password=password)
                auth_login(request, user)
                return redirect("index")
        else:
            form = RegistrationForm()
            context["form"] = form
        return render(request, 'registration/register.html', context)
    else:
        return redirect("index")


def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    if next is not None:
                        return redirect("index")
                    else:
                        return redirect("index")
        else:
            form = AuthenticationForm()
        context = {"form": form}
        return render(request, 'registration/login.html', context)
    else:
        return redirect("index")

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("login")


#class view_login(LoginView):
#    template_name = 'registration/login.html'

#def view_login(request):
    #if request.method == "POST":
        #loginform = LoginForm(request.POST)
        #if loginform.is_valid():
        #username = request.POST['username']
       # password = request.POST['password']
      #  user = authenticate(request, username=username, password=password)
     #   if user is not None:
    #        login(request, user)
   #     return HttpResponseRedirect(reverse("index"))
  #  else:
 #       loginform = LoginForm()
#    return render(request, "registration/login.html", {"form":loginform})

#def logout(request):
#    logout(request)
#    return redirect('login/')

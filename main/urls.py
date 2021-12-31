from django.urls import path
from . import views
#from django.conf.urls.static import static
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('explore/', views.explore, name='explore'),
    path('post/', views.post, name='post'),
    path('notification/', views.notification, name='notification'),
    path('like_post', views.like_post, name='like_post'),
    path('unlike_post', views.unlike_post, name='unlike_post'),
    path('account/', views.account, name='account'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path('followuser', views.follow_user, name='follow_user'),
    path('unfollowuser', views.unfollow_user, name='unfollow_user'),
    path('register/', views.register, name='register'),
]


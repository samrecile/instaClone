from django.urls import path
from . import views
#from django.conf.urls.static import static
from django.shortcuts import render, redirect


urlpatterns = [
    path('', views.index, name='index'),
    path('explore/', views.explore, name='explore'),
    path('notification/', views.notification, name='notification'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('upload/', views.upload, name='upload'),
]

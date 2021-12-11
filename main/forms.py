from django import forms
from .models import Profile, Image
from django.contrib.auth.models import User
from django.forms import ModelForm

class PostForm(forms.ModelForm):
  class Meta:
    model = Image
    fields = ('image_caption', 'image', 'tag_someone')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['bio','profile_pic','profile_avatar','date']

    
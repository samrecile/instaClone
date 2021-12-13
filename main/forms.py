from django import forms
from .models import Profile, Image
from django.contrib.auth.models import User
from django.forms import ModelForm

class PostForm(forms.ModelForm):
  class Meta:
    model = Image
    fields = ('image_caption', 'image', 'tag_someone')

  #def __init__(self, user, *args, **kwargs):
   #     self.imageuploader_profile = user
    #    super(PostForm, self).__init__(*args, **kwargs)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['bio','profile_pic','profile_avatar','date']

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)
    
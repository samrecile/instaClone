from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *

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

class UpdateProfile(forms.ModelForm):
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password')

class UpdateProfile2(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ('bio', 'profile_pic')




class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    #def save(self, commit=True):
     #   user = super(RegistrationForm, self).save(commit=False)
      #  user.first_name = self.cleaned_data['first_name']
       # user.last_name = self.cleaned_data['email']
#
 #       if commit:
  #          user.save()
        
   #     return User 

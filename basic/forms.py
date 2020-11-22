from django import forms
from django.contrib.auth.models import User
from .models import *

class UserProfileInfoForm(forms.ModelForm):
    
    class Meta():
        model = UserProfileInfo
        fields = ['profile_pic']

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ['content', 'video_clips', 'images', 'site_url']
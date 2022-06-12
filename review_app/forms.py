from django import forms
from .models import Profile, Project

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture')

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields=('title','image' ,'description','git_url' )
from rest_framework import serializers 
from .models import Project,Profile

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=('title', 'description', 'image','url')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=('user', 'image', 'bio')
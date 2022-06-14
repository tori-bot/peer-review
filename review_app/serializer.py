from rest_framework import serializers
from .models import Project, Profile


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('title', 'image', 'description',
                  'git_url', 'user', 'published', 'category')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'profile_picture', 'bio')

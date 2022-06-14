from urllib.request import Request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Profile, Project
from django.contrib.auth.models import User
from .forms import ProfileForm, ProjectForm
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# handle all the status code responses.
from .models import Profile, Project
from .serializer import ProjectSerializer, ProfileSerializer


# Create your views here.
@login_required(login_url='/accounts/login/')
def home(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    profile = Profile.get_profile_by_id(user.id)
    projects = Project.objects.all().order_by('-published')

    context = {
        'user': user,
        'profile': profile,
        'projects': projects
    }

    return render(request, 'home.html', context)

def technology(request):
    projects=Project.objects.filter(category='technology').order_by('-published')
    context={
        'projects': projects
    }
    return render(request,'technology.html',context)

def art(request):
    projects=Project.objects.filter(category='art').order_by('-published')
    context={
        'projects': projects
    }
    return render(request,'art.html',context)

def fashion(request):
    projects=Project.objects.filter(category='fashion').order_by('-published')
    context={
        'projects': projects
    }
    return render(request,'fashion.html',context)

def architecture(request):
    projects=Project.objects.filter(category='architecture').order_by('-published')
    context={
        'projects': projects
    }
    return render(request,'architecture.html',context)

def profile_form(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user=user)
    profile_form = ProfileForm()
    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()

            return redirect('home')
        else:
            return HttpResponse('Please fill the form correctly.')
    else:
        context = {
            'profile_form': profile_form,
        }
        return render(request, 'profile_form.html', context)


def profile(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    profile = Profile.get_profile_by_id(user.id)
# user's projects

    context = {
        'profile': profile,
        'user': user,
    }
    return render(request, 'profile.html', context)


@login_required
def search(request):
    if 'search' in request.GET and request.GET["search"]:
        search_term = request.GET.get("search")
        print(f'\n {search_term} \n')
        searched_profiles = Profile.search_profile(search_term)
        # print(searched_profiles)
        message = f"{search_term}"
        return render(request, 'search.html', {"message": message, "profiles": searched_profiles})
    else:
        message = "Take the chance to search for a profile"

    return render(request, 'search.html', {'message': message})


def user_profile(request, username):
    current_user = request.user
    user = User.objects.get(username=current_user.username)
    selected = User.objects.get(username=username)
    if selected == user:
        return redirect('home', username=current_user.username)

    context = {
        'profile': profile,
    }
    return render(request, 'user_profile.html', context)


def upload_project(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    profile = Profile.get_profile_by_id(user.id)
    upload = ProjectForm()
    if request.method == 'POST':
        upload = ProjectForm(request.POST, request.FILES)
        if upload.is_valid():
            upload.instance.user = current_user
            upload.save()
            return redirect('home')
        else:
            return HttpResponse('Please fill the form correctly')
    else:
        context = {
            'upload': upload,
            'user': user,
            'profile': profile
        }
        return render(request, 'upload_project.html', context)

# build api


class ProjectView(APIView):
    # APIView as a base class for our API view function.
    def get(self, request, format=None):
        # define a get method where we query the database to get all the objects
        all_projects = Project.objects.all()
        # print({all_projects})
        # all_projects=list(all_projects)
        # serialize the Django model objects and return the serialized data as a response.
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        # post method will be triggered when we are getting form data
        serializers = ProjectSerializer(data=request.data)
        # serialize the data in the request
        if serializers.is_valid():
            # If valid we save the new data to the database and return the appropriate status code.
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    # APIView as a base class for our API view function.
    def get(self, request, format=None):
        # define a get method where we query the database to get all the objects
        all_projects = Profile.objects.all()
        # serialize the Django model objects and return the serialized data as a response.
        serializers = ProfileSerializer(all_projects, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        # post method will be triggered when we are getting form data
        serializers = ProfileSerializer(data=request.data)
        # serialize the data in the request
        if serializers.is_valid():
            # If valid we save the new data to the database and return the appropriate status code.
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiList(APIView):

    def get(self, request, format=None):

        return render(request, "apis.html")

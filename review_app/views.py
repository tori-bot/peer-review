from urllib.request import Request
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Profile, Project,Comment
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

def about(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    profile = Profile.get_profile_by_id(user.id)
    
    context={
        'user': user,
        
        'profile': profile
    }
    return render(request,'about.html',context)

def technology(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    profile = Profile.get_profile_by_id(user.id)
    projects=Project.objects.filter(category='technology').order_by('-published')
    context={
        'user': user,
        'projects': projects,
        'profile': profile
    }
    return render(request,'technology.html',context)

def art(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    profile = Profile.get_profile_by_id(user.id)
    projects=Project.objects.filter(category='art').order_by('-published')
    context={
        'user': user,
        'projects': projects,
        'profile': profile
    }
    return render(request,'art.html',context)

def fashion(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    profile = Profile.get_profile_by_id(user.id)
    projects=Project.objects.filter(category='fashion').order_by('-published')
    context={
        'user': user,
        'projects': projects,
        'profile': profile
    }
    return render(request,'fashion.html',context)

def architecture(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    profile = Profile.get_profile_by_id(user.id)
    projects=Project.objects.filter(category='architecture').order_by('-published')
    context={
        'user': user,
        'projects': projects,
        'profile': profile
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
            'user': user,
            'profile': profile
        }
        return render(request, 'profile_form.html', context)


def profile(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    profile = Profile.get_profile_by_id(user.id)
    projects=Project.objects.filter(user=user.id).order_by('-published')

    context = {
        'profile': profile,
        'user': user,
        'projects': projects
    }
    return render(request, 'profile.html', context)


@login_required
def search(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    profile = Profile.get_profile_by_id(user.id)
    if 'search' in request.GET and request.GET["search"]:
        search_term = request.GET.get("search")
        print(f'\n {search_term} \n')
        searched_profiles = Profile.search_profile(search_term)
        message = f"{search_term}"    
    else:
        message = "Take this chance to search for a profile"

    context={
        'message': message,
        'profiles': searched_profiles,
        'user': user,
        'profile': profile
        }
    return render(request, 'search.html',context)


def user_profile(request, id):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    current_profile = Profile.get_profile_by_id(user.id)
    selected = get_object_or_404(User, id= id)
    print({selected})

    if selected == user:
        return redirect('profile', id=current_user.id)
    
    profile=Profile.get_profile_by_id(selected.id)
    projects=Project.objects.filter(user=selected.id)

    context = {
        'profile': profile,
        'projects': projects,
        'user': user,
        'current_profile': current_profile

    }
    return render(request, 'user_profile.html', context)


@login_required(login_url='/accounts/login/')
def single_project(request,pk):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    profile = Profile.get_profile_by_id(user.id)
    project=Project.objects.filter(id=pk).first()
    try:
        comments = Comment.objects.filter(project=project)
    except Comment.DoesNotExist:
        comments=None

    context = {
        'project':project,
        "comments":comments,
        'profile':profile,
        'user':user
        }
    
    return render(request,'single_project.html',context)  

@login_required(login_url='/accounts/login/')
def comment(request,project_id):
    current_user = request.user
    if request.method == 'POST':
        comment= request.POST.get('comment')
    project = Project.objects.get(id=project_id)
    user_profile = User.objects.get(username=current_user.username)
    new_comment,created=Comment.objects.get_or_create(
         content=comment,
         project = project,
         user=user_profile   
        )
    new_comment.save()

    return redirect('single_project' ,pk=project_id)
 

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

def project_update(request,project_id):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    profile = Profile.get_profile_by_id(user.id)
    project_id=int(project_id)
    try:
        updated=Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return redirect('home')
    project_form=ProjectForm(request.POST or None,instance=updated)
    if project_form.is_valid():
        project_form.save()
        return redirect('home')
    context={
        'project_form':project_form,
        'user':user,
        'profile':profile
    }
    return render(request, 'upload_project.html',context)

def delete_project(request,project_id):
    project_id=int(project_id)
    try:
        updated=Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return redirect('home')
    updated.delete()
    return redirect('home')


# build api


class ProjectView(APIView):
    # APIView as a base class for our API view function.
    def get(self, request, format=None):
        # define a get method where we query the database to get all the objects
        all_projects = Project.objects.all()

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
        current_user = request.user
        user = User.objects.get(id=current_user.id)
        profile = Profile.get_profile_by_id(user.id)
        context={
            'user': user,
            'profile': profile
        }
        return render(request, "apis.html",context)

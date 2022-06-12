from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Profile
from django.contrib.auth.models import User
from .forms import ProfileForm, ProjectForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    current_user = request.user
    user=User.objects.get(id=current_user.id)
    profile=Profile.get_profile_by_id(user.id)

    context={
        'user': user,
        'profile': profile,
    }

    return render(request, 'home.html',context)

def profile_form(request,id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user = user)
    profile_form=ProfileForm()
    if request.method == 'POST':
        profile_form=ProfileForm(request.POST,request.FILES,instance=profile)
        if profile_form.is_valid():
            profile_form.save()

            return redirect('home')
        else:
            return HttpResponse('Please fill the form correctly.')
    else:
        context={
            'profile_form': profile_form, 
        }
        return render(request,'profile_form.html',context)

def profile(request):
    current_user = request.user
    user=User.objects.get(id=current_user.id)
    profile=Profile.get_profile_by_id(user.id)
# user's projects

    context={
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
        return render(request, 'search.html', {"message":message,"profiles": searched_profiles})
    else:
        message = "Take the chance to search for a profile"

    return render(request, 'search.html', {'message': message})

def user_profile(request,username):
    current_user=request.user
    user=User.objects.get(username=current_user.username)
    selected=User.objects.get(username=username)
    if selected==user:
        return redirect('home',username=current_user.username)

    context={
        'profile':profile,
    }
    return render(request,'user_profile.html',context)

def upload_project(request):
    current_user=request.user
    upload=ProjectForm()
    if request.method == 'POST':
        upload=ProjectForm(request.POST,request.FILES)
        if upload.is_valid():
            upload.instance.user=current_user
            upload.save()
            return redirect('home')
        else:
            return HttpResponse('Please fill the form correctly')
    else:
        context={
            'upload': upload,
        }
        return render(request,'upload_project.html',context)

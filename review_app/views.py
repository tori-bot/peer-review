from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Profile
from django.contrib.auth.models import User
from .forms import ProfileForm

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
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Profile
from django.contrib.auth.models import User
from .forms import ProfileForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def profile_form(request,id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user = user)
    profile_form=ProfileForm()
    if request.method == 'POST':
        profile_form=ProfileForm(request.POST,request.FILES,instance=profile)
        if profile_form.is_valid():
            profile_form.save()

            return redirect('profile')
        else:
            return HttpResponse('Please fill the form correctly.')
    else:
        context={
            'profile_form': profile_form, 
        }
        return render(request,'profile_form.html',context)
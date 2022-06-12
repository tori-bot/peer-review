from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),

    path('profile_form/<int:id>/',views.profile_form,name='profile_form'),
]
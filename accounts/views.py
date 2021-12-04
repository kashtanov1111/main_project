import os

from django.shortcuts import render
from .forms import CustomUserCreationForm #, UserProfileinfoForm
from django.urls import reverse_lazy
from django.views import generic

from .models import CustomUser
from .forms import UserProfileForm, CustomUserChangeForm

def userprofile(request):
    if request.method == 'POST':
        profile_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
       
        if profile_form.is_valid():
            profile_form.save()
            #profile_form = profile_form.save(commit=False)  
            #profile_form.user = request.user
 
            #if 'profile_pic' in request.FILES:
            #    profile_form.profile_pic = request.FILES['profile_pic']
            #if request.FILES.get('profile_pic', None) != None:
            #    try:
            #        os.remove(request.user.profile_pic.url)
            #    except Exception as e:
            #        print('Exception in removing old profile image: ', e)
            #    request.user.profile_pic = request.FILES['profile_pic']
            #    request.user.save()
            
            #return render(request, 'home.html')
            return render(request, 'account/userprofile.html', {'profile_form': profile_form})
    else:
        profile_form = CustomUserChangeForm(instance=request.user)
    return render(request, 'account/userprofile.html', {'profile_form': profile_form})
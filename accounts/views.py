import os

from django.shortcuts import render
from .forms import CustomUserCreationForm #, UserProfileinfoForm
from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings
from allauth.account.views import LoginView
from .models import CustomUser
from .forms import UserProfileForm, CustomUserChangeForm, GuestForm
from django.shortcuts import redirect, render

from .models import GuestEmail

def userprofile(request):
    if request.method == 'POST':
        profile_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
       
        if profile_form.is_valid():
            #if settings.USE_S3:
            #    upload = Upload
            
            
            
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

def guest_login_view(request):
    form = GuestForm(request.POST or None)
    context = {
        'form': form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        return redirect(redirect_path)
    return redirect('/register/')

class CustomLoginView(LoginView):
    def form_valid(self, form):
        try:
            del self.request.session['guest_email_id']
        except:
            pass
        return super().form_valid(form)
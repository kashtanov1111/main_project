import os
from shutil import ReadError
from allauth.account.views import LoginView, SignupView

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import redirect, render
from django.views import generic
from django.views.generic import DetailView, View, FormView
from django.views.generic.edit import FormMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe

from .models import CustomUser, GuestEmail, EmailActivation
from .forms import UserProfileForm, ReactivateEmailForm, CustomUserChangeForm, GuestForm, CustomUserCreationForm, ProductsLoginForm
from config.mixins import NextUrlMixin

@login_required
def account_home_view(request):
    return render(request, 'accounts/home.html', {})

class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name='accounts/home.html'
    def get_object(self):
        return self.request.user

class AccountEmailActivateView(FormMixin, View):
    success_url = '/accounts/login/'
    form_class = ReactivateEmailForm
    key = None
    def get(self, request, key=None, *args, **kwargs):  
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, 'Your email has been confirmed. Please Login.' )
                return redirect('home')
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse('account_change_password')
                    msg = """Your email has already been confirmed
                    Do you need to <a href='{link}'>reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect('home')
        context = {'form': self.get_form(), 'key': key}
        return render(request, 'registration/activation-error.html', context)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = "Activation link sent, please check your email."
        messages.success(self.request, msg)
        email = form.cleaned_data.get('email')
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, 'key': self.key}
        return render(self.request, 'registration/activation-error.html', context)

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

# def guest_login_view(request):
#     form = GuestForm(request.POST or None)
#     context = {
#         'form': form
#     }
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         email = form.cleaned_data.get('email')
#         new_guest_email = GuestEmail.objects.create(email=email)
#         request.session['guest_email_id'] = new_guest_email.id
#         return redirect(redirect_path)
#     return redirect('/register/')

class GuestRegisterView(NextUrlMixin, FormView):
    form_class = GuestForm
    default_next = '/accounts/signup/'

    def form_invalid(self, form):
        return redirect(self.default_next)
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        self.request.session['guest_email_id'] = new_guest_email.id
        return redirect(self.get_next_url())

class CustomLoginView(LoginView):
    form_class = ProductsLoginForm
    def form_valid(self, form):
        try:
            del self.request.session['guest_email_id']
        except:
            pass
        return super().form_valid(form)

class CustomSignUpView(SignupView):
    def form_valid(self, form):
        self.user = form.save(self.request)
        return redirect('account_login')
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from allauth.account.forms import SignupForm, LoginForm
from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import CustomUser, GuestEmail
from .models import EmailActivation

class ReactivateEmailForm(forms.Form):
    email           = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse('account_signup')
            msg = """This email does not exists, would you like to <a href='{link}'>register</a>?
            """.format(link=register_link) 
            raise forms.ValidationError(mark_safe(msg))
        return email

class GuestForm(forms.ModelForm):
    class Meta:
        model = GuestEmail
        fields = [
            'email'
        ]
    
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        obj = super().save(commit=False)
        if commit:
            obj.save()
            request = self.request
            request.session['guest_email_id'] = obj.id
        return obj

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'username', 'age', 'city')

class CustomUserChangeForm(UserChangeForm):
    profile_pic = forms.ImageField(widget=forms.FileInput, required=False)
    password = None
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('email', 'username', 'age', 'city', 'portfolio_site', 'profile_pic')

class UserEcommerceDetailChangeForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name']

class CustomSignupForm(SignupForm):
    city = forms.CharField(max_length=100, required=False)
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.city = self.cleaned_data['city']
        # obj= EmailActivation.objects.create(user=user)
        # obj.send_activation()
        user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('age', 'city', 'portfolio_site', 'profile_pic')

class ProductsLoginForm(LoginForm):
    def clean(self):
        data = super().clean()
        request = self.request
        email = data.get('login')
        password = data.get('password')
        qs = CustomUser.objects.filter(email=email)
        if qs.exists():      
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                link = reverse('user:resend-activation')
                reconfirm_msg = """Go to
                    <a href='{resend_link}'>resend confirmation email</a>
                """.format(resend_link=link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = 'Please check your email to confirm your account or' + reconfirm_msg.lower()
                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_qs = EmailActivation.objects.email_exists(email)
                if email_confirm_qs.exists():
                    msg2 = 'Email not confirmed. ' + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and not email_confirm_qs.exists():
                    raise forms.ValidationError('This user is inactive.')
        return data
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from allauth.account.forms import SignupForm, LoginForm
from django import forms

from .models import CustomUser
from .models import EmailActivation

class GuestForm(forms.Form):
    email = forms.EmailField()

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
    pass
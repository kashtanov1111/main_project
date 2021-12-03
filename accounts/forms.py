from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from allauth.account.forms import SignupForm
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'username', 'age', 'city')

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('email', 'username', 'age', 'city')

class CustomSignupForm(SignupForm):
    city = forms.CharField(max_length=100, required=False)
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.city = self.cleaned_data['city']
        user.save()
        return user

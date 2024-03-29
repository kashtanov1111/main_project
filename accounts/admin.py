from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, GuestEmail, EmailActivation

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'age', 'city', 'is_staff', ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age', 'city', 'portfolio_site', 'profile_pic')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('age', 'city', 'portfolio_site', 'profile_pic' )}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(GuestEmail)
admin.site.register(EmailActivation)
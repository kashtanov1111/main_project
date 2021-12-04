from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import CustomURLValidator
from django.core import validators
# Create your models here.

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)

    portfolio_site = models.CharField(max_length=400, blank=True, validators=[CustomURLValidator()])
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)


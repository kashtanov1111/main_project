from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
from .validators import CustomURLValidator
from django.core import validators

class UserManager(UserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self.__db)
        return user_obj
    
    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user

class CustomUser(AbstractUser):
    email   = models.EmailField(max_length=255, unique=True)
    active  = models.BooleanField(default=True)
    staff   = models.BooleanField(default=False)
    admin   = models.BooleanField(default=False)
    age     = models.PositiveIntegerField(null=True, blank=True)
    city    = models.CharField(max_length=100, blank=True)

    portfolio_site = models.CharField(max_length=400, blank=True, validators=[CustomURLValidator()])
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email

    @property
    def is_admin(self):
        return self.admin

class GuestEmail(models.Model):
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

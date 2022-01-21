import email
from datetime import timedelta
from random import random
from sqlite3 import Timestamp
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
from django.core import validators
from django.core.mail import send_mail
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.template.loader import get_template
from django.utils import timezone
from django.urls import reverse

from .validators import CustomURLValidator
from config.utils import random_string_generator, unique_key_generator
# send_mail(subject, message, from_email, recipient_list, html_message)

DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 7)

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
        user_obj.is_active = is_active
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
    is_active  = models.BooleanField(default=True)
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

class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range = now
        return self.filter(
            activated = False,
            forced_expired = False
        ).filter(
            timestamp__gt=start_range,
            timestamp__lte=end_range
        )

class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(
            Q(email=email) | Q(user__email=email)
            ).filter(activated=False)


class EmailActivation(models.Model):
    user            = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email           = models.EmailField()
    key             = models.CharField(max_length=120, blank=True, null=True)
    activated       = models.BooleanField(default=False)
    forced_expired  = models.BooleanField(default=False)
    expires         = models.IntegerField(default=7)
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False
    
    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False



    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, 'BASE_URL')
                key_path = reverse('user:email-activate', kwargs={'key': self.key})
                path = '%s%s' % (base_url, key_path)
                context = {
                    'path': path,
                    'email': self.email
                }
                txt_ = get_template('registration/email/verify.txt').render(context)
                html_ = get_template('registration/email/verify.html').render(context)
                subject = '1-Click Email Verification'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]

                sent_mail = send_mail(
                    subject,
                    txt_,
                    from_email,
                    recipient_list,
                    html_message=html_,
                    fail_silently=False
                )
                return sent_mail
        return False



def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)

pre_save.connect(pre_save_email_activation, sender=EmailActivation)

def post_save_user_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()

post_save.connect(post_save_user_create_receiver, sender=CustomUser)

class GuestEmail(models.Model):
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

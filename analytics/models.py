from ast import Pass
from decimal import MAX_EMAX
from email.policy import default
from ipaddress import ip_address
from sqlite3 import Timestamp
from typing import Generic
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save

from .signals import object_viewed_signal
from .utils import get_client_ip
from allauth.account.signals import user_logged_in

User = settings.AUTH_USER_MODEL
class ObjectViewed(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address      = models.CharField(max_length=120, blank=True, null=True)  
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s viewed %s' %(self.content_object, self.timestamp)

    class Meta:
        ordering            = ['-timestamp']
        verbose_name        = 'Object viewed'
        verbose_name_plural = 'Objects viewed '


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    new_view_obj = ObjectViewed.objects.create(
        user = request.user,
        object_id = instance.id,
        ip_address = get_client_ip(request),
        content_type = c_type,
    )

object_viewed_signal.connect(object_viewed_receiver)

class UserSession(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address      = models.CharField(max_length=120, blank=True, null=True)  
    session_key     = models.CharField(max_length=100, null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    active          = models.BooleanField(default=True)
    ended          = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended


def post_save_session_receiver(sender, instance, created, *args, **kwargs ):
    if created:
        qs = UserSession.objects.filter(user=instance.user).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()

post_save.connect(post_save_session_receiver, sender=UserSession)

def user_logged_in_receiver(sender, user, request, *args, **kwargs):
    session_key = request.session.session_key
    ip_address = get_client_ip(request)
    user = user
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key,
    )
user_logged_in.connect(user_logged_in_receiver)
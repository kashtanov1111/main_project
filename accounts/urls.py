from django.urls import path

from .import views

urlpatterns = [
    path('profile', views.userprofile, name='user_profile'),
]

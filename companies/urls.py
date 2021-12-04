from django.urls import path

from . import views

app_name = 'companies'
urlpatterns = [
    path('', views.workers, name='workers'),
    path('users/', views.users, name='users'),
]



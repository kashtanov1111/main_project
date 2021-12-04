from django.urls import path

from . import views

app_name = 'first_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('form_page/', views.form_name_view, name='form'),
]

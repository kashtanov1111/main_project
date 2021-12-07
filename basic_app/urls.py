from django.urls import path

from . import views

app_name = 'basic_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('other/', views.other, name='other'),
    path('relative/', views.relative, name='relative'),
    path('home/', views.SchoolListView.as_view(), name='schools'),
    path('home/<int:pk>/', views.SchoolDetailView.as_view(), name='school_detail'),
    path('home/create/', views.SchoolCreateView.as_view(), name='create'),
    path('home/update/<int:pk>/', views.SchoolUpdateView.as_view(), name='update'),
    path('home/delete/<int:pk>/', views.SchoolDeleteView.as_view(), name='delete'),

]

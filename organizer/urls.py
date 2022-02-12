from urllib.parse import urlparse
from django.urls import path, re_path

from . import views

app_name = 'organizer'
urlpatterns = [
    path('', views.redirect_root),
    path('newslink/create/', views.NewsLinkCreate.as_view(), name='newslink_create'),
    path('newslink/update/<int:pk>/', views.NewsLinkUpdate.as_view(), name='newslink_update'),
    path('newslink/delete/<int:pk>/', views.NewsLinkDelete.as_view(), name='newslink_delete'),
    path('startup/', views.StartupList.as_view(), name='startup_list'),
    path('startup/create/', views.StartupCreate.as_view(), name='startup_create'),
    path('startup/<slug:slug>/', views.startup_detail, name='startup_detail'),
    path('startup/<slug:slug>/update/', views.StartupUpdate.as_view(), name='startup_update'),
    path('startup/<slug:slug>/delete/', views.StartupDelete.as_view(), name='startup_delete'),
    path('tag/', views.TagPageList.as_view(), name='tag_list'),
    path('tag/<int:page_number>/', views.TagPageList.as_view(), name='tag_page'),
    path('tag/create/', views.TagCreate.as_view(), name='tag_create'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),
    path('tag/<slug:slug>/update/', views.TagUpdate.as_view(), name='tag_update'),
    path('tag/<slug:slug>/delete/', views.TagDelete.as_view(), name='tag_delete'),
]

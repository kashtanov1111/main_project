from urllib.parse import urlparse
from django.urls import path, re_path

from . import views

app_name = 'sublog'
urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('create/', views.PostCreate.as_view(), name='post_create'),
    re_path(r'^(?P<year>[0-9]{4})/'
            r'(?P<month>[0-9]{1,2})/'
            r'(?P<slug>[\w-]+)/'
            r'delete/$', 
            views.PostDelete.as_view(),
            name='post_delete'),
    re_path(r'^(?P<year>[0-9]{4})/'
            r'(?P<month>[0-9]{1,2})/'
            r'(?P<slug>[\w-]+)/'
            r'update/$', 
            views.PostUpdate.as_view(),
            name='post_update'),
    re_path(r'^(?P<year>[0-9]{4})/'
            r'(?P<month>[0-9]{1,2})/'
            r'(?P<slug>[\w-]+)/$', 
            views.post_detail,
            name='post_detail'),
]

from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

urlpatterns = [
    path('note/<uuid:pk>/delete/', BlogDeleteView.as_view(), name='note_delete'),
    path('note/<uuid:pk>/edit/', BlogUpdateView.as_view(), name='note_edit'),
    path('note/new/', BlogCreateView.as_view(), name='note_new'),
    path('note/<uuid:pk>/', BlogDetailView.as_view(), name='note_detail'),
    path('', BlogListView.as_view(), name='blog'),
]

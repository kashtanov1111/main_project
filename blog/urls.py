from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

urlpatterns = [
    path('note/<int:pk>/delete/', BlogDeleteView.as_view(), name='note_delete'),
    path('note/<int:pk>/edit/', BlogUpdateView.as_view(), name='note_edit'),
    path('note/new/', BlogCreateView.as_view(), name='note_new'),
    path('note/<int:pk>/', BlogDetailView.as_view(), name='note_detail'),
    path('', BlogListView.as_view(), name='blog'),
]

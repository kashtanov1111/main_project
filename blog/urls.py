from django.urls import path
from .views import BlogListView, BlogDetailView

urlpatterns = [
    path('', BlogListView.as_view(), name='blog'),
    path('note/<int:pk>/', BlogDetailView.as_view(), name='note_detail'),
]

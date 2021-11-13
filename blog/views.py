from typing import List
from .models import Note
from django.views.generic import ListView, DetailView
# Create your views here.

class BlogListView(ListView):
    model = Note
    template_name = 'blog/blog.html'

class BlogDetailView(DetailView):
    model = Note
    template_name = 'blog/note_detail.html'
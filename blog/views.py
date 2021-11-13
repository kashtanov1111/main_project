from typing import List
from .models import Note
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Create your views here.

class BlogListView(ListView):
    model = Note
    template_name = 'blog/blog.html'

class BlogDetailView(DetailView):
    model = Note
    template_name = 'blog/note_detail.html'

class BlogCreateView(CreateView):
    model = Note
    template_name = 'blog/note_new.html'
    fields = ['title', 'author', 'body']

class BlogUpdateView(UpdateView):
    model = Note
    template_name = 'blog/note_edit.html'
    fields = ['title', 'body']

class BlogDeleteView(DeleteView):
    model = Note
    template_name = 'blog/note_delete.html'
    success_url = reverse_lazy('blog')

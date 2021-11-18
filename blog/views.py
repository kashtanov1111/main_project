from typing import List
from .models import Note, Comment
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class BlogListView(ListView):
    model = Note
    template_name = 'blog/blog.html'

class BlogDetailView(UserPassesTestMixin, DetailView):
    model = Note
    template_name = 'blog/note_detail.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user 

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = 'blog/note_new.html'
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    template_name = 'blog/note_edit.html'
    fields = ['title', 'body']

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user 

class BlogDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Note
    template_name = 'blog/note_delete.html'
    success_url = reverse_lazy('blog')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user 

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/leave_comment.html'
    fields = ['note', 'comment']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
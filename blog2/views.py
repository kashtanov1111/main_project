from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView, ListView,
                                    DetailView, CreateView,
                                    DeleteView, UpdateView)
from django.db.models import Q

from .models import Post, Comment
from .forms import CommentForm, PostForm

class AboutView(TemplateView):
    template_name = 'blog2/about.html'

class PostListView(ListView):
    model = Post
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(Q(published_date__isnull=False) | Q(published_date__isnull=True, author=self.request.user)).order_by('created_date')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostForm
    model = Post
    
    def test_func(self):
        return self.get_object().author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog2:post_list')

    def test_func(self):
        return self.get_object().author == self.request.user

class DraftListView(LoginRequiredMixin, ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True, author=self.request.user).order_by('created_date')
    

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog2:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog2/comment_form.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog2:post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog2:post_detail', pk=post_pk)

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog2:post_detail', pk=pk)
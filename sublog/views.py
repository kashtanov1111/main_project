from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.generic import (
    CreateView, ListView, View
)

from .models import Post
from .forms import PostForm

class PostList(ListView):
    model = Post

def post_detail(request, year, month, slug):
    post = get_object_or_404(
        Post,
        pub_date__year=year,
        pub_date__month=month,
        slug=slug
    )
    return render(
        request,
        'sublog/post_detail.html',
        {'post': post}
    )

class PostCreate(CreateView):
    form_class = PostForm
    model = Post


class PostUpdate(View):
    form_class = PostForm
    model = Post
    template_name = 'sublog/post_form_update.html'
    
    def get_object(self, year, month, slug):
        return get_object_or_404(
            self.model,
            pub_date__year=year,
            pub_date__month=month,
            slug=slug
        )

    def get(self, request, year, month, slug):
        post = self.get_object(year, month, slug)
        context = {
            'form': self.form_class(instance=post),
            'post': post
        }
        return render(request, self.template_name, context)

    def post(self, request, year, month, slug):
        post = self.get_object(year, month, slug)
        bound_form = self.form_class(
            request.POST, instance=post
        )
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        else:
            context = {
                'form': bound_form,
                'post': post
            }
            return render(
                request,
                self.template_name,
                context
            )

class PostDelete(View):

    def get(self, request, year, month, slug):
        post = get_object_or_404(
                Post,
                pub_date__year=year,
                pub_date__month=month,
                slug=slug)
        return render(
            request,
            'sublog/post_confirm_delete.html',
            {'post': post}
        )

    def post(self, request, year, month, slug):
        post = get_object_or_404(
                Post,
                pub_date__year=year,
                pub_date__month=month,
                slug=slug)
        post.delete()
        return redirect('sublog:post_list')
from ast import Delete
from django.core.paginator import (Paginator, 
                EmptyPage, PageNotAnInteger)
from django.views.generic import (
    CreateView, DeleteView, DetailView, UpdateView, View,
)
from django.shortcuts import (
    render, redirect, get_object_or_404)
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse, Http404
from django.urls import reverse_lazy, reverse

from .models import Tag, Startup, NewsLink
from .forms import TagForm, StartupForm, NewsLinkForm

class TagList(View):
    template_name = 'organizer/tag_list.html'

    def get(self, request):
        tags = Tag.objects.all()
        context = {
            'tag_list': tags
        }
        return render(
            request, self.template_name, context
        )

class TagPageList(View):
    paginate_by = 5
    template_name = 'organizer/tag_list.html'

    def get(self, request, page_number='a'):
        tags = Tag.objects.all()
        paginator = Paginator(tags, self.paginate_by)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        if page.has_previous():
            prev_url = reverse(
                'organizer:tag_page',
                args=(page.previous_page_number(),)
            )
        else:
            prev_url = None
        if page.has_next():
            next_url = reverse(
                'organizer:tag_page',
                args=(page.next_page_number(),)
            )
        else:
            next_url = None
        context = {
            'is_paginated': page.has_other_pages(),
            'next_page_url': next_url,
            'previous_page_url': prev_url,
            'paginator': paginator,
            'tag_list': page
        }
        return render(request, self.template_name, context)

class TagDetail(DetailView):
    model = Tag

class StartupList(View):
    page_kwarg = 'page'
    paginate_by = 5
    template_name = 'organizer/startup_list.html'

    def get(self, request):
        startups = Startup.objects.all()
        paginator = Paginator(startups, self.paginate_by)
        page_number = request.GET.get(self.page_kwarg)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        if page.has_previous():
            prev_url = '?{pkw}={n}'.format(
                pkw=self.page_kwarg,
                n=page.previous_page_number()
            )
        else:
            prev_url = None
        if page.has_next():
            next_url = '?{pkw}={n}'.format(
                pkw=self.page_kwarg,
                n=page.next_page_number()
            )
        else:
            next_url = None
        context = {
                'is_paginated': page.has_other_pages(),
                'startup_list': page,
                'paginator': paginator,
                'previous_page_url': prev_url,
                'next_page_url': next_url,
                }
        return render(request, self.template_name, context)

class StartupDetail(DetailView):
    model = Startup



# def tag_create(request):
#     if request.method == 'POST':
#         form = TagForm(request.POST)
#         if form.is_valid():
#             new_tag = form.save()
#             return redirect(new_tag)
#     else:
#         form = TagForm()
#     return render(
#         request,
#         'organizer/tag_form.html',
#         {'form': form}
#     )

class TagCreate(CreateView):
    form_class = TagForm
    model = Tag

class TagUpdate(UpdateView):
    form_class = TagForm
    model = Tag
    template_name = 'organizer/tag_form_update.html'

class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy('organizer:tag_list')

class StartupCreate(CreateView):
    form_class = StartupForm
    model = Startup

class StartupUpdate(UpdateView):
    form_class = StartupForm
    model = Startup
    template_name = 'organizer/startup_form_update.html'

class StartupDelete(DeleteView):
    model = Startup
    success_url = reverse_lazy('organizer:startup_list')

class NewsLinkCreate(CreateView):
    form_class = NewsLinkForm
    model = NewsLink

class NewsLinkUpdate(View):
    form_class = NewsLinkForm
    template_name = 'organizer/newslink_form_update.html'

    def get(self, request, pk):
        newslink = get_object_or_404(NewsLink, pk=pk)
        context = {
            'form': self.form_class(instance=newslink),
            'newslink': newslink,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        newslink = get_object_or_404(
            NewsLink, pk=pk
        )
        bound_form = self.form_class(
            request.POST, instance=newslink
        )
        if bound_form.is_valid():
            new_newslink=bound_form.save()
            return redirect(new_newslink)
        else:
            context = {
                'form': bound_form,
                'newslink': newslink
            }
            return render(
                request,
                self.template_name,
                context
            )

class NewsLinkDelete(View):

    def get(self, request, pk):
        newslink = get_object_or_404(
            NewsLink, pk=pk
        )
        return render(
            request,
            'organizer/newslink_confirm_delete.html',
            {'newslink': newslink}
        )
    
    def post(self, request, pk):
        newslink = get_object_or_404(
            NewsLink, pk=pk
        )
        startup = newslink.startup
        newslink.delete()
        return redirect(startup)
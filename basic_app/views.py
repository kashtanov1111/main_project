from django.shortcuts import render
from django.views.generic import (View, TemplateView, 
                                    ListView,CreateView, 
                                    DetailView, UpdateView,
                                    DeleteView,)
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from . import models

# Create your views here.
def index(request):
    context_dict = {'text': 'hello world', 'number': 100}
    return render(request, 'basic_app/index.html', context_dict)

def other(request):
    return render(request, 'basic_app/other.html')

def relative(request):
    return render(request, 'basic_app/relative_url_templates.html')

class SchoolListView(LoginRequiredMixin, ListView):
    model = models.School
    context_object_name = 'schools'
    template_name = 'basic_app/school_list.html'

class SchoolDetailView(LoginRequiredMixin, DetailView):
    model = models.School
    context_object_name = 'school_detail'
    template_name = 'basic_app/school_detail.html'

class SchoolCreateView(LoginRequiredMixin, CreateView):
    fields = ('name', 'principal', 'location')
    model = models.School

class SchoolUpdateView(LoginRequiredMixin, UpdateView):
    fields = ('name', 'principal')
    model = models.School

class SchoolDeleteView(LoginRequiredMixin, DeleteView):
    model = models.School
    success_url = reverse_lazy('basic_app:schools')
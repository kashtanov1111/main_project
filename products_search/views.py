from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q

from products.models import Product

class SearchProductView(ListView):
    template_name = 'search/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q', None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()
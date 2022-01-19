from typing import List
from django.http.response import Http404
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from analytics.mixins import ObjectViewedMixin
from products_carts.models import Cart
from .models import Product
from .forms import ContactForm

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': 'Contact',
        'content': 'Welcome to the contact page',
        'form': contact_form
    }
    if contact_form.is_valid():
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Thank you'})
    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return HttpResponse(errors, status=400, content_type='application/json')
    return render(request, 'products/contact_page.html', context)


class ProductListView(ListView):
    
    #def get_context_data(self, *args, **kwargs):
    #    context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #    return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()



class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404('Not found..')
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        # object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return instance

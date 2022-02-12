from typing import List
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import Http404, HttpResponse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View

from analytics.mixins import ObjectViewedMixin
from products_carts.models import Cart
from .models import Product, ProductFile
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
        print('haahha')
        request = self.request
        return Product.objects.all()

class UserProducHistoryView(LoginRequiredMixin, ListView):
    template_name = 'products/user-history.html'
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
        views = request.user.objectviewed_set.all().by_model(Product, model_queryset=False)
        # viewed_ids = [x.object_id for x in views]
        return views #Product.objects.filter(pk__in=viewed_ids)


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

import os
from wsgiref.util import FileWrapper
from django.conf import settings
from mimetypes import guess_type
from products_orders.models import ProductPurchase

class ProductDownloadView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        pk = kwargs.get('pk')
        downloads_qs = ProductFile.objects.filter(pk=pk, product__slug=slug)
        if downloads_qs.count() != 1:
            raise Http404('Download not found')
        download_obj = downloads_qs.first()
        can_download = False
        user_ready = True
        if download_obj.user_required:
            if not request.user.is_authenticated():
                user_ready = False
        purchased_products = Product.objects.none()
        if download_obj.free:
            can_download = True
            user_ready = True
        else:
            purchased_products = ProductPurchase.objects.products_by_request(request)
            if download_obj.product in purchased_products:
                can_download = True
        if not can_download or not user_ready:
            messages.error(request, 'You do not have access to download this item.')
            return redirect(download_obj.get_default_url())

        aws_filepath = download_obj.generate_download_url()
        return HttpResponseRedirect(aws_filepath)
        # file_root = settings.PROTECTED_ROOT
        # filepath = download_obj.file.path
        # final_filepath = os.path.join(file_root, filepath)
        # with open(final_filepath, 'rb') as f:
        #     wrapper = FileWrapper(f)
        #     mime_type = 'application/force-download'
        #     guessed_mimetype = guess_type(filepath)[0]
        #     if guessed_mimetype:
        #         mimetype = guessed_mimetype
        #     response = HttpResponse(wrapper, content_type=mime_type)
        #     response['Content-Disposition'] = 'attachment;filename=%s' % (download_obj.name)
        #     response['X-SendFile'] = str(download_obj.name)
        #     return response
from django.contrib.auth import login
from django.shortcuts import render, redirect

from products.models import Product
from .models import Cart
from products_orders.models import Order
from products_billing.models import BillingProfile
from accounts.forms import ProductsLoginForm, GuestForm
from accounts.models import GuestEmail
from products_addresses.forms import AddressForm
from products_addresses.models import Address

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, 'carts/home.html', {'cart': cart_obj })

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('products_carts:home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
    return redirect('products_carts:home')

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        redirect('products_carts:home')
    login_form = ProductsLoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        order_obj, order_object_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        elif billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()
    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'form':login_form,
        'next': '/products/cart/checkout/',
        'guest_form': guest_form,
        'address_form': address_form,
    }
    return render(request, 'carts/checkout.html', context)
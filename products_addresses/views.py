from django.shortcuts import render
from django.shortcuts import redirect

from .forms import AddressForm
from products_billing.models import BillingProfile
from products_addresses.models import Address

def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        'form': form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
            request.session[address_type + '_address_id'] = instance.id
        else:
            return redirect('products_carts:checkout') 

        return redirect(redirect_path)
    return redirect('products_carts:checkout') 

def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        context = {
        }
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if request.method == 'POST':
            shipping_address = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type + '_address_id'] = shipping_address
                    return redirect(redirect_path)
    return redirect('products_carts:checkout')  
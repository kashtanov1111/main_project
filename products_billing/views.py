from re import S
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from products_billing.models import BillingProfile, Card
import stripe
STRIPE_SECRET_KEY = getattr(settings, 'STRIPE_SECRET_KEY')
STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY' )
stripe.api_key = STRIPE_SECRET_KEY

def payment_method_view(request):
    # if request.user.is_authenticated:
    #     billing_profile = request.user.billingprofile
    #     my_customer_id = billing_profile.customer_id
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect('/products/cart/')
    next_url = None
    next_ = request.GET.get('next')
    next_url = next_
    return render(request, 'billing/payment-method.html', {'publish_key': STRIPE_PUB_KEY, 'next_url': next_url})

def payment_method_createview(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({'message': 'Cannot find this user'}, status_code=401)
        token = request.POST.get('token')
        if token is not None:
            # customer = stripe.Customer.retrieve(billing_profile.customer_id)
            # card_response = customer.sources.create(source=token)
            
            # card_response = stripe.Customer.create_source(
            #             billing_profile.customer_id,
            #             source=token,
            #             )
            # new_card_obj = Card.objects.add_new(billing_profile, card_response)
            new_card_obj = Card.objects.add_new(billing_profile, token)
        return JsonResponse({'message': 'Success! Your card was added.'})
    return HttpResponse("error", status_code=401)
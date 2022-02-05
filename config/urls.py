"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from analytics.views import SalesView, SalesAjaxView
from products_billing.views import payment_method_view, payment_method_createview
from accounts.views import GuestRegisterView, CustomLoginView, CustomSignUpView
from products_carts.views import cart_detail_api_view
from products_addresses.views import checkout_address_create_view, checkout_address_reuse_view
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView
from products_orders.views import LibraryView

urlpatterns = [
    path('admin-2281953/', admin.site.urls),
    path('accounts/signup/', CustomSignUpView.as_view(), name='account_signup'),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('accounts/', include('allauth.urls')),
    path('analytics/sales/', SalesView.as_view(), name='sales-analytics'),
    path('analytics/sales/data/', SalesAjaxView.as_view(), name='sales-analytics-data'),
    path('billing/payment-method/create/', payment_method_createview, name='billing-payment-method-endpoint'),
    path('billing/payment-method/', payment_method_view, name='billing-payment-method'),
    path('register/guest/', GuestRegisterView.as_view(), name='guest_register'),
    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'), 
    path('library /', LibraryView.as_view(), name='library'), 
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'), 
    path('user/', include('accounts.urls')),
    path('orders/', include('products_orders.urls')),
    path('polls/', include('polls.urls')),
    path('blog/', include('blog.urls')),
    path('blog2/', include('blog2.urls')),
    path('books/', include('books.urls')),
    path('doc/', include('doc.urls')),
    path('first_app/', include('first_app.urls')),
    path('companies/', include('companies.urls')),
    path('basic_app/', include('basic_app.urls')),
    path('groups/', include('groups.urls')),
    path('posts/', include('posts.urls')),
    path('api/cart/', cart_detail_api_view, name='api-cart'),
    path('products/cart/', include('products_carts.urls')),
    path('products/', include('products.urls')),
    path('settings/email/', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    path('webhooks/mailchimp/', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
    path('', include('pages.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
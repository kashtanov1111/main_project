from django.urls import path

from . import views

app_name = 'products_carts'
urlpatterns = [
    path('', views.cart_home, name='home'),
    path('checkout/success/', views.checkout_done_view, name='success'),
    path('checkout/', views.checkout_home, name='checkout'),
    path('update/', views.cart_update, name='update'),
]

from django.urls import path

from .import views
from products.views import UserProducHistoryView

app_name = 'user'
urlpatterns = [
    path('profile', views.userprofile, name='user_profile'),
    path('e-details', views.UserEcommerceDetailUpdateView.as_view(), name='e-user-update'),
    path('history/products/', UserProducHistoryView.as_view(), name='user-history-product'),
    path('ecommerce_profile', views.AccountHomeView.as_view(), name='user_ecommerce_profile'),
    path('email/confirm/<str:key>/', views.AccountEmailActivateView.as_view(), name='email-activate'),
    path('email/resend-activation/', views.AccountEmailActivateView.as_view(), name='resend-activation'),
]

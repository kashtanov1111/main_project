from django.urls import path

from .import views

app_name='orders'
urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),
    path('endpoint/verify/ownership/', views.VerifyOwnership.as_view(), name='verify-ownership'),
    path('<str:order_id>/', views.OrderDetailView.as_view(), name='detail'),
]

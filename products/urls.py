from django.urls import path, include

from . import views

app_name='products'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('search/', include('products_search.urls')),
    path('<slug:slug>/', views.ProductDetailSlugView.as_view(), name='detail'),   
]

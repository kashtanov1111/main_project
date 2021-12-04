from .views import HomePageView, XoxPageView, ConnectFourPageView, help
from django.urls import path

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('connect_four/', ConnectFourPageView.as_view(), name='connectfour'),
    path('xox/', XoxPageView.as_view(), name='xox'),
    path('help/', help, name='help_page'),
]

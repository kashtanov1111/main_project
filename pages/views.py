from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

class ConnectFourPageView(TemplateView):
    template_name = 'connectfour.html'

class XoxPageView(TemplateView):
    template_name = 'xox.html'
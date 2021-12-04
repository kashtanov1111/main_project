from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

class ConnectFourPageView(TemplateView):
    template_name = 'connectfour.html'

class XoxPageView(TemplateView):
    template_name = 'xox.html'

def help(request):
    context = {'help': 'We can help you!'}
    return render(request, 'help.html', context)
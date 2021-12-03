from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail

from .forms import UploadFileForm, ContactForm


def year_archive(request, year):
    return HttpResponse('%s this is year' % year)

def special_case_2003(request, foo):
    year = 5555
    return HttpResponseRedirect(reverse('year-archive', args=(year,)))
def month_archive(request, year, month):
    return HttpResponse('%s this is year and this is %s the month' % (year, month))

def article_detail(request, year, month, slug):
    return HttpResponse('%s this is year and this is %s the month and this is the slug: %s' % (year, month, slug))

def page(request, num=1):
    return HttpResponse('%s the page' % num)

def history(request, num, foo):
    return HttpResponse('%s history %s' % (num, foo))

def edit(request, num, foo):
    return HttpResponse('%s edit %s' % (num, foo))


def get_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipents = ['info@example.com']
            if  cc_myself:
                recipents.append(sender)
            send_mail(subject, message, sender, recipents)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def handle_upload_file(f):
    with open('folder/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_upload_file(request.FILES['file'])
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
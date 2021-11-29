from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse




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


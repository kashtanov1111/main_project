from django.urls import path, register_converter, re_path, include

from . import views, converters

register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('2003/', views.special_case_2003, {'foo': 'barrrrr'}),
    re_path(r'^(?P<year>[0-9]{4})/$', views.year_archive, name='year-archive'),
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    path('year<yyyy:year>/<int:month>/<slug:slug>/', views.article_detail),
    path('blog/', views.page),
    path('blog/page<int:num>/', views.page),
    path('<int:num>/', include([
        path('history/', views.history),
        path('edit/', views.edit),]), {'foo': 'baaaaar'}),
]

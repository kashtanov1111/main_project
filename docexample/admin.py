from django.contrib import admin

from .models import Place, Restaurant, Waiter

admin.site.register(Waiter)
admin.site.register(Restaurant)
admin.site.register(Place)

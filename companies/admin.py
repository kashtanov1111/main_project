from django.contrib import admin

from .models import Worker, Company, User

admin.site.register(Worker)
admin.site.register(Company)
admin.site.register(User)
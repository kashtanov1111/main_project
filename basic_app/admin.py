from django.contrib import admin

from .models import School, Student

admin.site.register(Student)
admin.site.register(School)

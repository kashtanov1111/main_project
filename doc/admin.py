from django.contrib import admin

from .models import Student, Card, Medal, Moon

class StudentAdmin(admin.ModelAdmin):
    list_display = ['year_in_school', 'is_upperclass']

admin.site.register(Student, StudentAdmin)
admin.site.register(Card)
admin.site.register(Medal)
admin.site.register(Moon)
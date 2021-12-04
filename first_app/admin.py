from django.contrib import admin

# Register your models here.
from .models import AccessRecord, Topic, Webpage

admin.site.register(Topic)
admin.site.register(AccessRecord)
admin.site.register(Webpage)
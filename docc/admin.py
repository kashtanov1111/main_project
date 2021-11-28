from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.db.models.base import Model

from .models import Manufacturer, Car, Student, Topping, Pizza, Person, Other, Group, Membership, Place, Restaurant, Waiter

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer')


admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Car, CarAdmin)

class ToppingAdmin(admin.ModelAdmin):
    list_display = ('name',)

class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_toppings')

    def get_toppings(self, obj):
        return ' '.join([t.name for t in obj.toppings.all()])

admin.site.register(Topping, ToppingAdmin)
admin.site.register(Pizza, PizzaAdmin)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'baby_boomer_status')

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_members')

    def get_members(self, obj):
        return ', '.join([m.name for m in obj.members.all()])

admin.site.register(Person, PersonAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Membership, )


admin.site.register(Place)
admin.site.register(Restaurant)
admin.site.register(Waiter)
admin.site.register(Other)

admin.site.register(Student)
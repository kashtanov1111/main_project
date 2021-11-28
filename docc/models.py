from django.db import models
from django.db.models.deletion import CASCADE

from blog.models import Note

class Manufacturer(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)

######################

class Topping(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Pizza(models.Model):
    name = models.CharField(max_length=20)
    toppings = models.ManyToManyField(Topping)

################

class Person(models.Model):
    name = models.CharField(max_length=128)
    birth_date = models.DateField(blank=True, null=True)

    def baby_boomer_status(self):
        import datetime
        if self.birth_date < datetime.date(1945, 8, 1):
            return 'Pre-boomer'
        elif self.birth_date < datetime.date(1965, 1, 1):
            return 'Baby boomer'
        else:
            return 'Post-booomer'

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=CASCADE)
    group = models.ForeignKey(Group, on_delete=CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

#########################

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return '%s the place' % self.name

class Restaurant(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True)
    serves_hot_dogs = models.BooleanField(default=False)
    selves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return '%s the restaurant' % self.place.name

class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return '%s the water at %s' % (self.name, self.restaurant)

###########################

class Other(models.Model):
    name = models.ForeignKey(Note, on_delete=CASCADE)

class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True

class Student(CommonInfo):
    name = None
    home_group = models.CharField(max_length=5)
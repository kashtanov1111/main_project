from django.db import models
from django.db.models.deletion import CASCADE

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return "%s the place" % self.name
    
class Restaurant(models.Model):
    place = models.OneToOneField(Place, on_delete=CASCADE, primary_key=True)
    serves_hot_dogs = models.BooleanField(default=False)
    seves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return '%s the restaurant' % self.place.name

class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return '%s is the waiter at %s' % (self.name, self.restaurant)
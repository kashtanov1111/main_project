from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime

class ModelFormWithFileField(models.Model):
    file = models.FileField()

class Student(models.Model):
    
    class YearInSchool(models.TextChoices):
        FRESHMAN = 'FR'#, _('Freshman')
        SOPHOMORE = 'SO'#, _('Sophomore')
        JUNIOR = 'JR'#, _('Junior')
        SENIOR = 'SR'#, _('Senior')
        GRADUATE = 'GR'#, _('Graduate')

    year_in_school = models.CharField(max_length=2, choices=YearInSchool.choices, default=YearInSchool.FRESHMAN)

    def is_upperclass(self):
        return self.year_in_school in {self.YearInSchool.JUNIOR, self.YearInSchool.SENIOR} 

class Card(models.Model):

    class Suit(models.IntegerChoices):
        DIAMOND = 1
        SPADE = 2
        HEART = 3
        CLUB = 4

    suit = models.IntegerField(choices=Suit.choices)

class Medal(models.Model):
    MedalType = models.TextChoices('MedalType', 'GOLD SILVER BRONZE')

    medal = models.CharField(max_length=10, choices=MedalType.choices)

class Moon(models.Model):

    class MoonLandings(datetime.date, models.Choices):
        APOLLO_11 = 1969, 7, 20, 'Apollo 11 (Eagle)'
        APOLLO_12 = 1969, 11, 19, 'Apollo 12 (Intrepid)'
        APOLLO_14 = 1971, 2, 5, 'Apollo 14 (Antares)'
        APOLLO_15 = 1971, 7, 30, 'Apollo 15 (Falcon)'
        APOLLO_16 = 1972, 4, 21, 'Apollo 16 (Orion)'
        APOLLO_17 = 1972, 12, 11, 'Apollo 17 (Challenger)'

    apollo = models.DateField(max_length=15, choices=MoonLandings.choices)
import uuid
import datetime
from dateutil.relativedelta import relativedelta
from enum import unique
from django.db import models
from django.utils.text import slugify


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, unique=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, help_text='Enter your nickname', unique=True, null=True)
    
    SEX = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    sex = models.CharField(max_length=1, choices=SEX, blank=True, null=True)

    class ChildrenAmount(models.IntegerChoices):
        ONE = 1, '1'
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
    #ChildrenAmount = models.IntegerChoices('ChildrenAmount', 'ONE TWO THREE FOUR FIVE')
    childrens = models.IntegerField(choices=ChildrenAmount.choices, blank=True, null=True)
    from_usa = models.BooleanField(default=False)
    birthday = models.DateField(blank=True, null=True)
    weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    time_under_water = models.DurationField(verbose_name='Under Water time', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    filee = models.FileField(upload_to='files/%Y/%m/%d', blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    slug = models.SlugField(allow_unicode=True, blank=True, null=True)
    about_yourself = models.TextField(blank=True, null=True)
    birth_time = models.TimeField(blank=True, null=True)
    your_site = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.first_name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.first_name

class Article(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Person, on_delete=models.CASCADE, 
                        null=True,limit_choices_to={'birthday__lte': 
                        datetime.date.today() - relativedelta(years=18)})

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(Person, through='Membership', through_fields=('team', 'user'))

class Membership(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    inviter = models.ForeignKey(Person , on_delete=models.CASCADE, related_name='membership_invites', null=True)

class SpecialPerson(models.Model):
    first_name = models.OneToOneField(Person, on_delete=models.CASCADE)
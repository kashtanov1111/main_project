from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.company_name

class Worker(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class User(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=264, unique=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
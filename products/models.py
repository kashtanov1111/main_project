from django.db import models

class Product(models.Model):
    title        = models.CharField(max_length=120)
    description  = models.TextField()
    

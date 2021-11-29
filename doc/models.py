from django.db import models

class ModelFormWithFileField(models.Model):
    file = models.FileField()

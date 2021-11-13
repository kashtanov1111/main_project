from django.db import models

# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
    )
    date_time = models.DateTimeField()
    body = models.TextField()
    
    def __str__(self):
        return self.title
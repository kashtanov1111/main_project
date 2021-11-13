from django.db import models
from django.urls import reverse
# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
    )
    date_time = models.DateTimeField(auto_now=True)
    body = models.TextField()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('note_detail', args=[str(self.id)])
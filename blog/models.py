from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

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

class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('blog')
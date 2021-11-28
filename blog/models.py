import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

class Note(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
    )
    date_time = models.DateTimeField(auto_now=True)
    body = models.TextField()

    class Meta:
        ordering = ['-date_time']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('note_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.title == 'My my blog':
            return
        else:
            models.Model.save(self, *args, **kwargs)

    def last_updated(self):
        delta_time = timezone.now() - self.date_time
        if delta_time.days > 1:
            return '%s days ago' % delta_time.days
        else:
            if delta_time.seconds < 60:
                return '%s seconds ago' % delta_time.seconds
            if delta_time.seconds < 60 * 60:
                return '%s minutes ago' % (delta_time.seconds // 60)
            if delta_time.seconds < 60 * 60 * 24:
                return '%s hours ago' % (delta_time.seconds // 3600)
            
        

class Comment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('blog')


from django.db import models
from django.urls import reverse

from organizer.models import Tag, Startup

class Post(models.Model):
    title = models.CharField(max_length=63)
    slug = models.SlugField(
        max_length=63,
        help_text='A label for URL config.',
        unique_for_month='pub_date'
    )
    text = models.TextField()
    pub_date = models.DateField(
        'date published',
        auto_now_add=True,
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='blog_posts')
    startups = models.ManyToManyField(
        Startup,
        blank=True,
        related_name='blog_posts')

    def __str__(self):
        return '{}:{}'.format(
            self.title,
            self.pub_date.strftime('%Y-%m-%d')
        )

    def get_absolute_url(self):
        return reverse('sublog:post_detail', 
                        kwargs={
                            'year': self.pub_date.year,
                            'month': self.pub_date.month,
                            'slug': self.slug
                        })

    def get_update_url(self):
        return reverse('sublog:post_update', 
                        kwargs={
                            'year': self.pub_date.year,
                            'month': self.pub_date.month,
                            'slug': self.slug
                        })

    def get_delete_url(self):
        return reverse('sublog:post_delete', 
                        kwargs={
                            'year': self.pub_date.year,
                            'month': self.pub_date.month,
                            'slug': self.slug
                        })
    

    class Meta:
        verbose_name = 'blog post'
        ordering = ['-pub_date', 'title']
        get_latest_by = 'pub_date'
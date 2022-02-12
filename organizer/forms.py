from django import forms
from django.core.exceptions import ValidationError

from .models import Tag, Startup, NewsLink

class SlugCleanMixin:

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError(
                'Slug may not be "create".'
            )
        return new_slug

class TagForm(SlugCleanMixin, forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['name', 'slug']

    def clean_name(self):
        return self.cleaned_data['name'].lower()

    
class NewsLinkForm(forms.ModelForm):

    class Meta:
        model = NewsLink
        fields = ['title', 'pub_date', 'link', 'startup']
        
class StartupForm(SlugCleanMixin, forms.ModelForm):

    class Meta:
        model = Startup
        fields = ['name', 'slug', 'description', 'founded_date', 'contact', 'website', 'tags']

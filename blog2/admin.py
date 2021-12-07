from django.contrib import admin

# Register your models here.
from .models import Post, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline,]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
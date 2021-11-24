from django.contrib import admin
from .models import Note, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class NoteAdmin(admin.ModelAdmin):
    inlines = [ CommentInline,]
    list_display = ('title', 'author', 'date_time')

admin.site.register(Note, NoteAdmin)
admin.site.register(Comment)

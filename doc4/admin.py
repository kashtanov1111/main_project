from django.contrib import admin

from .models import Person, Article, Team, Membership, SpecialPerson

class ArticleInline(admin.TabularInline):
    model = Article
    extra = 0

class PersonAdmin(admin.ModelAdmin):
    inlines = [ArticleInline,]
    list_display = ('first_name', 'birthday')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_members')

    def get_members(self, object):
        return  ', '.join(k.first_name for k in object.members.all())

admin.site.register(Person, PersonAdmin)
admin.site.register(Article)
admin.site.register(Team, TeamAdmin)
admin.site.register(Membership)
admin.site.register(SpecialPerson)
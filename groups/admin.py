from django.contrib import admin

from .models import Group, GroupMember

class GroupMemberInline(admin.TabularInline):
    model = GroupMember
    extra = 0

class GroupAdmin(admin.ModelAdmin):
    inlines = [GroupMemberInline,]
    list_display = ('name', 'slug', 'description', 'description_html')
    fields = ['name', 'description', 'slug']
    search_fields = ['name', 'description']
    list_filter = ['name']

admin.site.register(GroupMember)
admin.site.register(Group, GroupAdmin)

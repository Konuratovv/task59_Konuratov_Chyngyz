from django.contrib import admin

from webapp.models import Issue, Type, Status, IssueType


class IssueTrackerAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'status', 'created_at']
    list_display_links = ['id', 'summary']
    search_fields = ['summary', 'description']
    fields = ['summary', 'description', 'status', 'created_at']
    filter_horizontal = ('types', )
    readonly_fields = ['created_at']


admin.site.register(Issue, IssueTrackerAdmin)
admin.site.register(Status)
admin.site.register(Type)

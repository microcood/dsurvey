from django.contrib import admin
from django.contrib.auth.models import *
from django.contrib.admin.models import LogEntry

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_filter = ('action_time', 'object_repr', 'action_flag')

from django.contrib import admin
from .models import LogSearch, LogSite

@admin.register(LogSite)
class LogSiteAdmin(admin.ModelAdmin):
    list_display = ('site', 'user', 'created_at')

@admin.register(LogSearch)
class LogSearchAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'result', 'user', 'created_at')
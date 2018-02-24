from django.contrib import admin
from .models import LogSearch, LogSite, LogPoint, LogAPISearch

@admin.register(LogSite)
class LogSiteAdmin(admin.ModelAdmin):
    list_display = ('site', 'user', 'created_at')

@admin.register(LogSearch)
class LogSearchAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'result', 'user', 'created_at')

@admin.register(LogPoint)
class LogPointAdmin(admin.ModelAdmin):
    list_display = ('user', 'point', 'how', 'created_at')

@admin.register(LogAPISearch)
class LogAPISearchAdmin(admin.ModelAdmin):
    list_display = ('url', 'result', 'created_at')
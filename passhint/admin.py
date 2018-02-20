from django.contrib import admin
from .models import Site, Rule, RuleSet, ReportSite, ReportRuleSet

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_url', 'created_at')

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'regex', 'desc_ko', 'created_at')

@admin.register(RuleSet)
class RuleSetAdmin(admin.ModelAdmin):
    list_display = ('site', 'user', 'created_at')

@admin.register(ReportSite)
class ReportSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_url', 'user', 'status', 'created_at')

@admin.register(ReportRuleSet)
class ReportRuleSetAdmin(admin.ModelAdmin):
    list_display = ('site', 'user', 'status', 'created_at')
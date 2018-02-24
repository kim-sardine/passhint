from django.contrib import admin

from .models import Site, Rule, RuleSet

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_url', 'created_at')

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'regex', 'desc_ko', 'created_at')

@admin.register(RuleSet)
class RuleSetAdmin(admin.ModelAdmin):
    list_display = ('site', 'user', 'created_at')

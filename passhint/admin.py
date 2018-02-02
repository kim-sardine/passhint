from django.contrib import admin
from .models import Site, Rule, RuleSet

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'rule_set', 'main_url', 'created_at')

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'regex', 'desc_ko', 'created_at')

@admin.register(RuleSet)
class RuleSetAdmin(admin.ModelAdmin):
    list_display = ('user', 'len_min', 'exc_special', 'created_at')
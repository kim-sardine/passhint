from django.contrib import admin
from django.db.models import F

from .models import Site, Rule, RuleSet, ReportSite, ReportRuleSet
from .common import RULE_LIST, POINT_DICT

# XXX RULE SENSITIVE
def approve_ruleset(modeladmin, request, queryset):
    for report_ruleset in queryset:

        new_ruleset = RuleSet()
        for rule in RULE_LIST:
            rule_value = getattr(report_ruleset, rule)
            setattr(new_ruleset, rule, rule_value)
        
        new_ruleset.user = report_ruleset.user
        new_ruleset.site = report_ruleset.site
        new_ruleset.save()

        reporter_profile = report_ruleset.user.profile
        reporter_profile.point = F('point') + POINT_DICT['ruleset_report']
        reporter_profile.save()
        reporter_profile.refresh_from_db()
approve_ruleset.short_description = "Approve this Report"

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
    actions = [approve_ruleset,]
    list_display = ('site', 'user', 'status', 'created_at')
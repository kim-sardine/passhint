from django.contrib import admin

from .models import ReportSite, ReportRuleSet
from passhint.models import RuleSet
from passhint.common import RULE_LIST

def approve_site(modeladmin, request, queryset):
    for report_ruleset in queryset:

        report_ruleset.status = 'approved'
        report_ruleset.save()

        reporter_profile = report_ruleset.user.profile
        reporter_profile.set_point('site_approved')
approve_site.short_description = "Approve this Report"

def reject_site(modeladmin, request, queryset):
    for report_ruleset in queryset:

        report_ruleset.status = 'rejected'
        report_ruleset.save()

        reporter_profile = report_ruleset.user.profile
        reporter_profile.set_point('site_rejected')
reject_site.short_description = "Reject this Report"

def late_site(modeladmin, request, queryset):
    for report_ruleset in queryset:

        report_ruleset.status = 'late'
        report_ruleset.save()

        reporter_profile = report_ruleset.user.profile
        reporter_profile.set_point('site_late')
late_site.short_description = "this Report is late"


@admin.register(ReportSite)
class ReportSiteAdmin(admin.ModelAdmin):
    actions = [approve_site, reject_site, late_site,]
    list_display = ('name', 'main_url', 'user', 'status', 'created_at')

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

        report_ruleset.status = 'approved'
        report_ruleset.save()

        reporter_profile = report_ruleset.user.profile
        reporter_profile.set_point('ruleset_approved')
approve_ruleset.short_description = "Approve this Report"

def reject_ruleset(modeladmin, request, queryset):
    for report_ruleset in queryset:

        report_ruleset.status = 'rejected'
        report_ruleset.save()

        reporter_profile = report_ruleset.user.profile
        reporter_profile.set_point('ruleset_rejected')
reject_ruleset.short_description = "Reject this Report"

def late_ruleset(modeladmin, request, queryset):
    for report_ruleset in queryset:

        report_ruleset.status = 'late'
        report_ruleset.save()

        reporter_profile = report_ruleset.user.profile
        reporter_profile.set_point('ruleset_late')
late_ruleset.short_description = "this Report is late"

@admin.register(ReportRuleSet)
class ReportRuleSetAdmin(admin.ModelAdmin):
    actions = [approve_ruleset, reject_ruleset, late_ruleset,]
    list_display = ('site', 'user', 'status', 'created_at')
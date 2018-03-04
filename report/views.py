from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from passhint.models import Site
from passhint.common import POINT_DICT

from .models import ReportRuleSet
from .forms import ReportSiteForm, ReportRuleSetForm
    
MAXIMUM_REPORT_RULESET_NUMBER = 10

# 사이트 등록 요청
@login_required
def report_site(request):
  
    if request.method == 'POST':
        form = ReportSiteForm(request.POST)

        if form.is_valid():
            report_site = form.save(commit=False)
            report_site.user = request.user
            report_site.save()

            reporter_profile = request.user.profile
            reporter_profile.set_point('Site : report')

            messages.success(request, _('Report complete! It takes time to review.'))
            return redirect('main')
        else:
            messages.error(request, _('Invalid form. Please try agiain'))
    else:    
        form = ReportSiteForm(label_suffix='')

    name = request.GET.get('name', '')
    url = request.GET.get('url', '')

    return render(request, 'report/report_site.html', {
        'form' : form,
        'name' : name,
        'url' : url,
        'point_dict': POINT_DICT,
        'nav_report_site' : 'active',
    })


# 사이트에 대한 RuleSet 등록
@login_required
def report_ruleset(request, site_name):
    
    site = get_object_or_404(Site.objects.prefetch_related('rule_sets'), name=site_name)

    # 최대 Report-RuleSet 갯수 : 10개 / 1일
    if ReportRuleSet.get_count_recent_1day(request.user) >= MAXIMUM_REPORT_RULESET_NUMBER:
        messages.warning(request, _('You can report up to 10 per day'))
        return redirect('passhint:site_detail', site_name=site_name)

    if request.method == 'POST':
        form = ReportRuleSetForm(request.POST)

        if form.is_valid():
            ruleset = form.save(commit=False)
            ruleset.user = request.user
            ruleset.site = site
            ruleset.save()

            reporter_profile = request.user.profile
            reporter_profile.set_point('Passhint : report')

            messages.warning(request, _('Report complete!'))
            return redirect('passhint:site_detail', site_name=site_name)
        else:
            messages.error(request, _('Invalid form. Please try agiain'))
    else:
        old_ruleset = site.get_recent_ruleset
        form = ReportRuleSetForm(instance=old_ruleset, label_suffix='')

    return render(request, 'report/report_ruleset.html', {
        'form' : form,
        'site' : site,
        'point_dict' : POINT_DICT,
    })

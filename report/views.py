from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from passhint.models import Site
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
            reporter_profile.set_point('site_report')

            # TODO Report Success Message : 제보 완료.. 등록까지 시간이 걸려요
            return redirect('main')
    else:    
        form = ReportSiteForm()

    name = request.GET.get('name', '')
    url = request.GET.get('url', '')

    return render(request, 'report/report_site.html', {
        'form' : form,
        'name' : name,
        'url' : url,
        'nav_report_site' : 'active',
    })

# TODO passhint 확인 가이드가 필요할 듯
# 사이트에 대한 RuleSet 등록
@login_required
def report_ruleset(request, site_name):
    
    site = get_object_or_404(Site.objects.prefetch_related('rule_sets'), name=site_name)

    # 최대 Report-RuleSet 갯수 : 10개 / 1일
    if ReportRuleSet.get_count_recent_1day(request.user) >= MAXIMUM_REPORT_RULESET_NUMBER:
        # TODO 한도 초과 Message : 하루 최대 10개까지 제보 가능합니다
        return redirect('passhint:site_detail', site_name=site_name)
                
    if request.method == 'POST':
        form = ReportRuleSetForm(request.POST)

        if form.is_valid():
            ruleset = form.save(commit=False)
            ruleset.user = request.user
            ruleset.site = site
            ruleset.save()

            reporter_profile = request.user.profile
            reporter_profile.set_point('ruleset_report')

            # TODO Report Success Message : 제보 완료..
            return redirect('passhint:site_detail', site_name=site_name)
    else:    
        form = ReportRuleSetForm()

    return render(request, 'report/report_ruleset.html', {
        'form' : form,
        'site' : site,
    })

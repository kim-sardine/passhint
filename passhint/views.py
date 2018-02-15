from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count

import json

from .models import Site, Rule, RuleSet
from .forms import SiteSearchForm, ReportSiteForm, ReportRuleSetForm

MAXIMUM_REPORT_RULESET_NUMBER = 10

# 메인 페이지
# 서비스 이름으로 passhint 를 검색하고
# 입력에 따라 auto complete를 도와주기
# 우측에 인기 검색어를 보여주기
def main(request):
    
    if request.method == 'POST':
    
        form = SiteSearchForm(request.POST)

        if form.is_valid():

            site_name = form.cleaned_data.get('site_name')
            try:
                site = Site.objects.get(name=site_name)
            except Site.DoesNotExist:
                response = redirect('passhint:site_search')
                response['Location'] += '?q='+site_name
                return response
            else:
                return redirect('passhint:site_detail', site_name=site_name)

    else:    
        form = SiteSearchForm()

    return render(request, 'passhint/main.html', {
        'form' : form,
    })


def site_search(request):
        
    q = request.GET.get('q')

    # TODO 검색 방식
    # 현재 : 태그 icontain 검색
    sites = Site.objects.filter(Q(tag__icontains = q)).prefetch_related('rule_sets').order_by('name')
    
    return render(request, 'passhint/site_search.html', {
        'sites' : sites,
    })


def site_detail(request, site_name):
    
    site = get_object_or_404(Site.objects.prefetch_related('rule_sets').select_related('user'), name=site_name)

    return render(request, 'passhint/site_detail.html', {
        'site' : site,
        })
    
# 사이트 등록 요청
@login_required
def site_report(request):
  
    if request.method == 'POST':
        form = ReportSiteForm(request.POST)

        if form.is_valid():
            report_site = form.save(commit=False)
            report_site.user = request.user
            report_site.save()

            # TODO Report Success Message : 제보 완료.. 등록까지 시간이 걸려요
            return redirect('passhint:main')
    else:    
        form = ReportSiteForm()

    return render(request, 'passhint/site_report.html', {
        'form' : form,
    })

# TODO passhint 확인 가이드가 필요할 듯
# 사이트에 대한 RuleSet 등록
@login_required
def site_report_ruleset(request, site_name):
    
    site = get_object_or_404(Site.objects.prefetch_related('rule_sets'), name=site_name)

    # 최대 Report-RuleSet 갯수 : 10개 / 1일
    if RuleSet.get_count_recent_1day(request.user) >= MAXIMUM_REPORT_RULESET_NUMBER:
        # TODO 한도 초과 Message : 하루 최대 10개까지 제보 가능합니다
        return redirect('passhint:site_detail', site_name=site_name)
                
    if request.method == 'POST':
        form = ReportRuleSetForm(request.POST)

        if form.is_valid():
            ruleset = form.save(commit=False)
            ruleset.user = request.user
            ruleset.site = site
            ruleset.save()

            # TODO Report Success Message : 제보 완료..
            return redirect('passhint:site_detail', site_name=site_name)
    else:    
        form = ReportRuleSetForm()

    return render(request, 'passhint/site_report_ruleset.html', {
        'form' : form,
        'site' : site,
    })


@csrf_exempt
def autocomplete(request):
    
    q = request.GET.get('term', '')

    # 서비스 중 인 site 중 검색하여 name으로 group_by 한 후 name 만 사용한다
    sites = Site.objects.filter(Q(tag__icontains = q)).order_by('name')

    results = [site.name for site in sites]
    
    return JsonResponse(results, safe=False)
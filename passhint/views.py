from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Count
from django.urls import reverse

import json

from .models import Site, Rule, RuleSet
from .forms import SiteSearchForm
from log.models import LogSearch, LogSite
from accounts.models import Profile


def get_user_or_none(user):
    return user if user.is_authenticated else None

# 메인 페이지
# 서비스 이름으로 passhint 를 검색하고
# 입력에 따라 auto complete를 도와주기
# 우측에 인기 검색어를 보여주기
def main(request):
    
    if request.method == 'POST':
    
        form = SiteSearchForm(request.POST)

        if form.is_valid():

            user = get_user_or_none(request.user)

            keyword = form.cleaned_data.get('keyword')
            try:
                site = Site.objects.get(name=keyword)
            except Site.DoesNotExist: 
                # name 으로 일치되는 것이 없으면 태그에서 완전일치 하는 것이 있는지 검사
                found_site = Site.get_site_by_tag(keyword)
                
                if found_site is None: # 태그로 완전일치가 없거나 다수 존재하면 search 로 이동
                    return HttpResponseRedirect(reverse('passhint:site_search') + '?q='+keyword)
                else: # 완전 일치하는 것이 딱 하나 존재하면 detail 로 이동
                    # 로그 저장
                    LogSearch.save_log_search(user, keyword, found_site)
                    return redirect('passhint:site_detail', site_name=found_site.name)
            else:
                # 로그 저장
                LogSearch.save_log_search(user, keyword, site)
                return redirect('passhint:site_detail', site_name=keyword)

    else:    
        form = SiteSearchForm()


    MAIN_ITEM_NUMBER = 7

    # hit 기준 정렬
    all_time_ranking = Site.objects.all().order_by('-hit')[:MAIN_ITEM_NUMBER]

    # log 모델 필요
    this_weak_ranking = LogSite.get_sorted_site_recent_nday(7)[:MAIN_ITEM_NUMBER]
    # today_ranking
    
    # created at 기준 정렬
    new_site_list = Site.objects.all().order_by('name')[:MAIN_ITEM_NUMBER]
    
    # log created at 기준 정렬
    # recent_search_list

    # hit 기준 정렬
    best_passhinter = Profile.objects.all().order_by('-point')[:MAIN_ITEM_NUMBER]

    return render(request, 'passhint/main.html', {
        'form' : form,
        'nav_main' : 'active',
        'all_time_ranking' : all_time_ranking,
        'this_weak_ranking' : this_weak_ranking,
        'new_site_list' : new_site_list,
        'best_passhinter' : best_passhinter,
    })


def site_search(request):
        
    keyword = request.GET.get('q')
    ordey_by = request.GET.get('ordey_by', 'name')

    if keyword:
        # TODO 검색 방식
        # 현재 : 태그 icontain 검색
        sites = Site.objects.filter(Q(tag__icontains = keyword)).prefetch_related('rule_sets').order_by(ordey_by)

        # 로그 저장
        user = get_user_or_none(request.user)
        LogSearch.save_log_search(user, keyword, sites)
    else:
        keyword = 'All site'
        sites = Site.objects.all().prefetch_related('rule_sets').order_by(ordey_by)

    
    return render(request, 'passhint/site_search.html', {
        'keyword' : keyword,
        'sites' : sites,
        'nav_site_search' : 'active',
    })


def site_detail(request, site_name):
    
    site = get_object_or_404(Site.objects.prefetch_related('rule_sets').select_related('user'), name=site_name)
    
    # hit++
    site.set_hit_plus_1()

    user = get_user_or_none(request.user)

    # 로그 저장
    LogSite.save_log_site(site, user)

    return render(request, 'passhint/site_detail.html', {
        'site' : site,
        })

@csrf_exempt
def autocomplete(request):
    
    q = request.GET.get('term', '')

    # 서비스 중 인 site 중 검색하여 name으로 group_by 한 후 name 만 사용한다
    sites = Site.objects.filter(Q(tag__icontains = q)).order_by('name')

    results = [site.name for site in sites]
    
    return JsonResponse(results, safe=False)

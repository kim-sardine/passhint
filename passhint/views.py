from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Site, Rule, RuleSet
from .forms import SiteSearchForm

def wow(request):
    
    return HttpResponse('hello')

def site_search(request):
        
    q = request.GET.get('q')

    # TODO 검색 방식
    # 약한 검사
    sites = Site.objects.filter(tag__icontains=q, status='service').order_by('name')

    return render(request, 'passhint/site_search.html', {
        'sites' : sites,
    })


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
                # 강력한 검사
                site = Site.objects.get(name__iexact = site_name, status='service')
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

def site_detail(request, site_name):
    
    return render(request, 'passhint/site_detail.html', {
        'site_name' : site_name,
    })


@csrf_exempt
def autocomplete(request):
    
    q = request.GET.get('term', '')
    sites = Site.objects.filter(tag__icontains = q, status='service')[:10]
    results = []

    for site in sites:
        results.append(site.name)
    
    return JsonResponse(results, safe=False)
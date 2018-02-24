from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from passhint.models import Site, RuleSet
from log.models import LogAPISearch

class passhint(APIView):

    def get(self, request, format=None):

        url = request.query_params.get('url')

        # SEARCH SITE BY URL
        search_result = Site.search_by_url(url)
        results = []
        log_site_name_list = []

        # GET TRUE RULESET
        for site in search_result:
            ruleset = site.get_recent_ruleset
            if ruleset:
                rule_list = ruleset.get_true_rule_list
                result = {'name' : site.name, 'rule_list' : rule_list}
                results.append(result)

                log_site_name_list.append(site.name)

        # 검색 결과 로그 저장
        log_site_name_string = ','.join(log_site_name_list)
        LogAPISearch.save_log_api_search(url, log_site_name_string)
        
        # RETURN THEM
        if results:
            return JsonResponse({'results' :results}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'results': 'error'}, status=status.HTTP_404_NOT_FOUND)

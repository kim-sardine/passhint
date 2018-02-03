from django.shortcuts import render
from django.http import HttpResponse
from .models import Site, Rule, RuleSet
def wow(request):
    return HttpResponse('hello')


def search(request):
    q = request.GET.get('q')

    site = Site.objects.get(tag__icontains=q)

    context = {
        'site' : site,
    }

    return render(request, 'passhint/search.html', context)
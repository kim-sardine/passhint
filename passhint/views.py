from django.shortcuts import render
from django.http import HttpResponse

def wow(request):
    return HttpResponse('hello')
from django.urls import path, re_path, include
from . import views

app_name = 'report'
urlpatterns = [
    path('', views.report_site, name='report_site'),
    path('<str:site_name>/',
         views.report_ruleset, name='report_ruleset'),
]

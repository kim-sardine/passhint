from django.urls import path, re_path, include
from . import views

app_name = 'passhint'
urlpatterns = [
    path('search/', views.site_search, name='site_search'),

    path('autocomplete/', views.autocomplete, name='autocomplete'),

    path('<str:site_name>/', views.site_detail, name='site_detail'),
]
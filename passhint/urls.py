from django.urls import path, re_path, include
from . import views

app_name = 'passhint'
urlpatterns = [
    path('', views.main, name='main'),
    path('wow/', views.wow, name='wow'),
    path('search/', views.site_search, name='site_search'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),

    path('<str:site_name>/', views.site_detail, name='site_detail')
]
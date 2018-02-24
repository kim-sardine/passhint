from django.urls import path, re_path, include
from . import views

app_name = 'api_v1'
urlpatterns = [
    path('passhint/', views.passhint.as_view(), name='passhint'),
]

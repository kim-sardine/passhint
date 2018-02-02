from django.urls import path, re_path, include
from . import views

app_name = 'passhint'
urlpatterns = [
    path('wow/', views.wow, name='wow'),
]
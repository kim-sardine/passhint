from django.conf import settings
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('social/signup/', views.MySignupView.as_view(), name='signup'),
]
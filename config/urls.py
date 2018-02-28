from django.conf import settings
from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from passhint.views import main
from accounts.views import profile
from config.settings.base import get_secret

urlpatterns = [
    path('', main, name='main'),
    path('passhint/', include('passhint.urls')),
    path('report/', include('report.urls')),

    path('api_v1/', include('api_v1.urls')),
    
    path('profile/<str:username>/', profile, name='profile'),

    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path( get_secret("ADMIN_URL") +'/', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

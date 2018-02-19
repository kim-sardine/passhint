from django.conf import settings
from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from passhint.views import main
from accounts.views import profile

urlpatterns = [
    path('', main, name='main'),
    path('passhint/', include('passhint.urls')),
    
    path('profile/<str:username>/', profile, name='profile'),

    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
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

# accounts/views.py
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as auth_login
from django.shortcuts import redirect, render
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.views import SignupView
from allauth.socialaccount.templatetags.socialaccount import get_providers
from .forms import SignupForm, LoginForm, t_SignupForm


class MySignupView(SignupView):
    template_name = ('accounts/signup_form.html')

@login_required
def profile(request):
    current_user = request.user
    # report_new_list = ReportNew.objects.filter(user=current_user)
    # report_update_list = ReportUpdate.objects.filter(user=current_user)
            # 'report_new_list' : report_new_list,
            # 'report_update_list' : report_update_list
    return render(request, 'accounts/profile.html', {
            'user' : current_user,
        })


def login(request):
    providers = []
    for provider in get_providers():  # settings/INSTALLED_APPS 내에서 활성화된 목록
        # social_app속성은 provider에는 없는 속성입니다.
        try:
            # 실제 Provider 별 Client id/secret 이 등록이 되어있는가?
            provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)

    return auth_login(request,
        authentication_form=LoginForm,
        template_name='accounts/login_form.html',
        extra_context={'providers': providers})
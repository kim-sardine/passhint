# accounts/views.py
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as auth_login
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.views import SignupView
from allauth.socialaccount.templatetags.socialaccount import get_providers

from .forms import SignupForm, LoginForm, t_SignupForm
from report.models import ReportRuleSet, ReportSite


class MySignupView(SignupView):
    template_name = ('accounts/signup_form.html')


def set_report_class(report_list):
    for report in report_list:
        if report.status == 'approved':
            setattr(report, 'class', 'list-group-item-primary')
        elif report.status == 'rejected':
            setattr(report, 'class', 'list-group-item-danger')
        elif report.status == 'late':
            setattr(report, 'class', 'list-group-item-warning')
        else:
            setattr(report, 'class', '')
    
    return report_list

# TODO 본인일 떄 체크해서 정보 수정 메뉴 보여주기
@login_required
def profile(request, username):

    user = get_object_or_404(get_user_model(), username=username)

    report_rulesets = ReportRuleSet.objects.filter(user=user)
    
    # 제보한 RuleSet 별로 승인 상태를 보여주기 위해 class 속성 설정
    report_rulesets = set_report_class(report_rulesets)

    report_sites = ReportSite.objects.filter(user=user)

    # 제보한 Site 별로 승인 상태를 보여주기 위해 class 속성 설정
    report_sites = set_report_class(report_sites)

    return render(request, 'accounts/profile.html', {
            'user' : user,
            'report_rulesets' : report_rulesets,
            'report_sites' : report_sites
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

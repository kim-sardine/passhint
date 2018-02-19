from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from .forms import t_SignupForm


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_login_redirect_url(self, request):
        # do your logic here for different social accounts
        ...
        return redirect('root')
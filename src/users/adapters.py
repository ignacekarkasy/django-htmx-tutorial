from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.shortcuts import resolve_url


class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_signup_redirect_url(self, request):
        return resolve_url(settings.SIGNUP_REDIRECT_URL)

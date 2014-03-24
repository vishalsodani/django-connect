from django.conf import settings
from django.contrib.auth import logout as django_logout

from django.http import HttpResponseRedirect
from django.shortcuts import render

from django_connect.decorators import anonymous_only


@anonymous_only
def welcome(request):
    return render(request, 'auth/welcome.html')


@anonymous_only
def login(request):
    return render(request, 'auth/login.html')


def logout(request):
    next = request.GET.get('next')
    django_logout(request)
    return HttpResponseRedirect(next or settings.LOGOUT_REDIRECT_URL)


@anonymous_only
def logged_out(request):
    return render(request, 'auth/logged_out.html')
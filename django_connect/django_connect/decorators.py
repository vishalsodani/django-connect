from threading import Thread

from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper


def anonymous_only(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_anonymous():
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    return wrap
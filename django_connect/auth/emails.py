from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django_connect.decorators import async


@async
def welcome(user):
    message = _("""
    Dear %(short_name)s,

    Welcome to Django Connect

    Django Connect
    """)
    context = {
        'short_name': user.get_short_name(),
    }
    send_mail(
        _('Welcome to Django Connect'),
        message % context,
        'no-reply@creco.co',
        [user.new_email.email],
        fail_silently=False,
    )
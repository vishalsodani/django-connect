from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django_connect.decorators import async


@async
def verify_email(user):
    message = _("""
    Dear %(short_name)s,

    Use the following link to verify your email:
    %(site_url)s%(page_url)s?email=%(email)s&key=%(key)s

    Django Connect
    """)
    context = {
        'short_name': user.get_short_name(),
        'email': user.new_email.email,
        'key': user.new_email.key,
        'site_url': settings.SITE_URL,
        'page_url': reverse('account:verify_email'),
    }
    send_mail(
        _('Verify your email'),
        message % context,
        'no-reply@creco.co',
        [user.new_email.email],
        fail_silently=False,
    )
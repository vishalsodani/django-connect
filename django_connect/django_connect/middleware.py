import pytz

from django.conf import settings
from django.utils import timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
			try:
				timezone.activate(pytz.timezone(tzname))
			except:
				timezone.deactivate()
        else:
            timezone.deactivate()
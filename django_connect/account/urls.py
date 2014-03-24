from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^settings/$', 'account.views.settings', name='settings'),
    url(r'^verify_email/$', 'account.views.verify_email', name='verify_email'),
)
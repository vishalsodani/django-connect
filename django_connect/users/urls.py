from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^me/$', 'users.views.me', name='me'),
)
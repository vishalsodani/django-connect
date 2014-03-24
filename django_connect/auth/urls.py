from django.conf.urls import patterns, url


urlpatterns = patterns('',
	url(r'^welcome/$', 'auth.views.welcome', name='welcome'),
    url(r'^login/$', 'auth.views.login', name='login'),
    url(r'^logout/$', 'auth.views.logout', name='logout'),
	url(r'^logged_out/$', 'auth.views.logged_out', name='logged_out'),
)
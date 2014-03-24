from django.conf.urls import patterns, url

from .views import CustomOAuthRedirect, CustomOAuthCallback

urlpatterns = patterns('',
    url(r'^login/(?P<provider>(\w|-)+)/$', CustomOAuthRedirect.as_view(), name='allaccess-login'),
    url(r'^callback/(?P<provider>(\w|-)+)/$', CustomOAuthCallback.as_view(), name='allaccess-callback'),
)
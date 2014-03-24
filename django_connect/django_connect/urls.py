from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'auth.views.welcome', name='home'), # change this to something else that redirects to welcome with if not logged in

    url(r'^account/', include('account.urls', namespace='account', app_name='account')),
    url(r'^auth/', include('auth.urls', namespace='auth', app_name='auth')),
    url(r'^users/', include('users.urls', namespace='users', app_name='users')),

    # django all access
    url(r'^connect/', include('connect.urls')),
    # django admin
    url(r'^admin/', include(admin.site.urls)),
)

# Serve static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    
    import debug_toolbar
    
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
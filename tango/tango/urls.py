from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from registration.backends.simple.views import RegistrationView


class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return '/rango/add_profile'


urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^rango/', include('rango.urls')),
                       url(r'^accounts/', include('registration.backends.simple.urls')),
                       url(r'^accounts/register/$', MyRegistrationView.as_view(), name='register_profile'),
                       url(r'^accounts/password_change/$',
                           'django.contrib.auth.views.password_change',
                           {'post_change_redirect': '/accounts/password_change/done/$'},
                           name="password_change_form"),
                       url(r'^accounts/password_change/done/$',
                           'django.contrib.auth.views.password_change_done', name='password_change_done'),

)
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT}), )

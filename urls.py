# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from admin import admin_site
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),

    # base
    url(r'^', include('base.urls')),

    # studies
    # url(r'^studies/', include('studies.urls')),

    # map
    url(r'^map/$', "studies.views.mapper", name="map"),

    # keyboard
    url(r'^keyboard/(?P<input_id>\w+)$', "studies.views.ipa_keyboard",
        name="keyboard_args"),
    url(r'^keyboard/$', "studies.views.ipa_keyboard",
        name="keyboard"),

    # grid
    url(r'^grid/', "studies.views.grid", name="grid"),

    # i18n
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # admin
    url(r'^admin/', include(admin_site.urls)),

    # login
    url(r'^admin/', 'django.contrib.auth.views.login', name="login"),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        # static server
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),

        # static media server
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
   )

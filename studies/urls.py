# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('studies.views',

    # index
    url(r'^$', 'search', name='search'),
    url(r'^ipa_keyboard/$', 'ipa_keyboard', name='ipa_keyboard'),

)

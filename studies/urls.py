# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('studies.views',

    # index
    url(r'^$', 'search', name="search"),

)

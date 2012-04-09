# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.sites.models import Site

from olwidget.admin import GeoModelAdmin

from base.models import GeospatialReference, MediaReference
from base.admin import GeospatialReferenceAdmin, MediaReferenceAdmin

from studies.models import Study, Language, Speaker, Production
from studies.admin import (ProductionAdmin, StudyAdmin, LanguageAdmin,
                           SpeakerAdmin)


class AdminSite(admin.AdminSite):

    def has_permission(self, request):
        return request.user.is_superuser or request.user.is_staff


def setup_admin():
    admin_site.register(User, UserAdmin)
    admin_site.register(Group, admin.ModelAdmin)
    admin_site.register(Site, admin.ModelAdmin)

    admin_site.register(GeospatialReference, GeospatialReferenceAdmin)
    admin_site.register(MediaReference, MediaReferenceAdmin)

    admin_site.register(Study, StudyAdmin)
#    admin_site.register(Language, LanguageAdmin)
    admin_site.register(Speaker, SpeakerAdmin)
    admin_site.register(Production, ProductionAdmin)

admin_site = AdminSite(name=settings.PROJECT_NAME)
setup_admin()

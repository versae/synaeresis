# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.gis.maps.google import GoogleMap
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from guardian.admin import GuardedModelAdmin
from olwidget.admin import GeoModelAdmin
from olwidget.widgets import MapDisplay, InfoMap

from base.models import GeospatialReference
from base.widgets import GoogleImagesSearchInput, OlWidgetGoogleMapsSearch

#GMAP = GoogleMap(key=settings.GOOGLE_MAPS_API_KEY)

class BaseAdmin(GuardedModelAdmin):
    user_can_access_owned_objects_only = True
    exclude = ('user', )
    save_on_top = True

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class GeospatialReferenceAdminForm(forms.ModelForm):

    class Meta:
        model = GeospatialReference

    def __init__(self, *args, **kwargs):
        super(GeospatialReferenceAdminForm, self).__init__(*args, **kwargs)
        attrs = {
            'size': 68,
            'class': 'olwidgetgooglemapssearch olwidget_maps:geometry,point',
        }
        self.fields['address'].widget = OlWidgetGoogleMapsSearch(attrs=attrs)

    def clean_geometry(self):
        geometry = self.cleaned_data['geometry']
        try:
            if isinstance(geometry, (tuple, list)):
                coords = geometry[0].point_on_surface.get_coords()
            else:
                coords = geometry.point_on_surface.get_coords()
        except:
            msg = _("Areas have to be plain (with no intersections).")
            raise forms.ValidationError(msg)
        return geometry


class GeospatialReferenceAdmin(BaseAdmin, GeoModelAdmin):

    class Media:
        js = (
            'http://openlayers.org/api/2.11/OpenLayers.js',
            'http://openstreetmap.org/openlayers/OpenStreetMap.js',
            '%solwidget/js/olwidget.js' % settings.MEDIA_URL,
            'http://maps.google.com/maps?file=api&v=3&key=%s&sensor=true' \
            % settings.GOOGLE_MAPS_API_KEY
        )
        css = {'all': ('%solwidget/css/olwidget.css' % settings.MEDIA_URL, )}

    form = GeospatialReferenceAdminForm
    verbose_name = _(u"References")
    ordering = ('title', )
    fieldsets = (
            (None, {
                'fields': ('title', 'address', 'geometry'),
            }),
            (_(u'More info'), {
                'classes': ('collapse', ),
                'fields': ('point', 'description'),
            }),
    )
    search_fields = ('title', 'address', 'description')
    list_display = ('title', 'address', 'ubication_map')
    list_per_page = 10
    # Does not work with GeometryCollection
    # list_map = ('geometry', )
    options = {
        'layers': [
            'osm.mapnik',  # 'osm.osmarender',
#            've.road', 've.shaded', 've.aerial', 've.hybrid'
#            'google.physical', 'google.hybrid', 'google.streets',
#            'google.satellite',
         ],
        'map_options': {
            'controls': ['Navigation', 'PanZoom',  # 'LayerSwitcher', 
                         'Attribution', 'Scale', 'ScaleLine'],
            'zoom': 10,
         },
         "default_zoom": 3,
         # 'geometry': ['point', 'polygon'],
         # 'is_collection': False,
    }
    # Does not work with GeometryCollection
    # Cluster points and regions
    # list_map_options = options
    # list_map_options.update({
    #     'cluster': True,
    #     'cluster_display': 'list',
    # })

    def ubication_map(self, obj):
        info = [u""]
        try:
            if obj.geometry:
                geo = obj.geometry
                coords = geo.point_on_surface.get_coords()
            elif obj.point:
                geo = obj.point
                coords = geo.get_coords()
            info = [(geo, "%s %s" % (_(u"On surface"), coords))]
        except:
            return u""
        options = {
            'layers': [
                'osm.mapnik',  # 'osm.osmarender',
#                'google.streets'
            ],
            'map_div_Style': {'width': '400px', 'height': '250px'},
        }
        map_display = InfoMap(info, options)
        return mark_safe(map_display.render(obj.title, {}))
    ubication_map.short_description = _(u"Ubication")
    ubication_map.allow_tags = True

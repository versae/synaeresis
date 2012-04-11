# -*- coding: utf-8 -*-
from magic import Magic

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.translation import gettext as _


class MediaReference(models.Model):
    title = models.CharField(_(u'Title'), max_length=200)
    file = models.FileField(_(u'File'), upload_to='images',
                            blank=True, null=True)
    url = models.URLField(_(u'URL'), verify_exists=False,
                          blank=True, null=True)
    excerpt = models.CharField(_(u'Excerpt'), max_length=200,
                               help_text=_("Time of a video or audio file, "
                                           "or boundaries in pixels for "
                                           "images. "
                                           "Time format: HH:MM:SS "
                                           "Pixels format: x1,y1;x2,y2."),
                               blank=True, null=True)
    user = models.ForeignKey(User, verbose_name=_("user"),
                             related_name="media")
    notes = models.TextField(_(u'Notes'), blank=True, null=True)

    def __unicode__(self):
        if self.file:
            return u"%s (%s)" % (self.title, self.file.name)
        elif self.url:
            return u"%s (%s)" % (self.title, self.url)
        else:
            return u"%s (%s)" % (self.title, self.url or self.image.url)

    def get_player(self, id=None):
        if id:
            id_attr = u" id=\"%s\"" % id
        else:
            id_attr = u" id=\"%s\"" % self.id
        if self.file:
            output = u"<a%s href='%s'>%s</a>" \
                     % (id_attr, self.file.url, self.file.name)
            get_mimetype = Magic(mime=True)
            mimetype = get_mimetype.from_file(self.file.path)
            if mimetype:
                main_type = mimetype.split("/")[0]
                if main_type == "audio":
                    output = u"<audio%s src='%s' preload='none' type='%s'></audio>" \
                             % (id_attr, self.file.url, mimetype)
                elif main_type == "video":
                    output = u"<video%s src='%s' preload='none' type='%s'></video>" \
                             % (id_attr, self.file.url, mimetype)
                elif main_type == "image":
                    output = u"<img%s src='%s'/>" \
                             % (id_attr, self.file.url, self.file.name)
        elif self.url:
            output = u"<a%s href='%s'>%s</a>" \
                     % (id_attr, self.url, self.title)
        else:
            output = u"%s" % self.title
        return output

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains", )


class BibliographicReference(models.Model):
    title = models.TextField(_(u'Title'))
    authors = models.TextField(_(u'Authors'), blank=True, null=True)
    url = models.URLField(_(u'URL'), verify_exists=False, blank=True,
                          null=True)
    isbn = models.CharField(_(u'ISBN'), max_length=60, blank=True,
                            null=True)
    user = models.ForeignKey(User, verbose_name=_("user"),
                             related_name="bibliography")
    notes = models.TextField(_(u'Notes'), blank=True, null=True)

    def __unicode__(self):
        return self.title


class GeospatialReference(models.Model):
    title = models.CharField(_('Title'), max_length=250, unique=True)
    address = models.CharField(_('Address'), max_length=250, blank=True,
                               null=True)
    geometry = models.MultiPolygonField(_('Geometry'), blank=True, null=True)
    point = models.PointField(_('Point'), blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    date = models.DateTimeField(_('Date'), auto_now=True)
    user = models.ForeignKey(User, verbose_name=_("user"),
                             related_name="locations")
    objects = models.GeoManager()

    def __unicode__(self):
        return u"%s" % self.title

    def save(self, *args, **kwargs):
        if (self.geometry and self.point
            and not self.geometry.contains(self.point)):
            self.point = self.geometry.point_on_surface
        if not self.point:
            self.point = self.geometry.point_on_surface
        super(GeospatialReference, self).save(*args, **kwargs)

    def get_valid_point(self):
        valid_point = None
        if self.geometry:
            valid_point = self.geometry.point_on_surface
        elif self.point:
            valid_point = self.point
        return valid_point

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains", )


class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()
    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    mpoly = models.MultiPolygonField()
    objects = models.GeoManager()

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name

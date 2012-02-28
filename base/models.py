# -*- coding: utf-8 -*-
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
    notes = models.TextField(_(u'Notes'), blank=True, null=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.title, self.url or self.image.url)


class BibliographicReference(models.Model):
    title = models.TextField(_(u'Title'))
    authors = models.TextField(_(u'Authors'), blank=True, null=True)
    url = models.URLField(_(u'URL'), verify_exists=False, blank=True,
                          null=True)
    isbn = models.CharField(_(u'ISBN'), max_length=60, blank=True,
                            null=True)
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

    objects = models.GeoManager()

    def __unicode__(self):
        if self.address:
            return u"%s (%s)" % (self.title, self.address)
        else:
            return u"%s" % self.title

    def save(self, *args, **kwargs):
        if (self.geometry and self.point
            and not self.geometry.contains(self.point)):
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
        return ("id__iexact", "title__icontains",)

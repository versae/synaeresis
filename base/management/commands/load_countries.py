import os
from django.contrib.gis.utils import LayerMapping
from base.models import WorldBorder, GeospatialReference
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError



class Command(BaseCommand):

    def handle(self, *args, **options):
        world_mapping = {
            'fips' : 'FIPS',
            'iso2' : 'ISO2',
            'iso3' : 'ISO3',
            'un' : 'UN',
            'name' : 'NAME',
            'area' : 'AREA',
            'pop2005' : 'POP2005',
            'region' : 'REGION',
            'subregion' : 'SUBREGION',
            'lon' : 'LON',
            'lat' : 'LAT',
            'mpoly' : 'MULTIPOLYGON',
        }

        world_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '_data/TM_WORLD_BORDERS-0.3.shp'))


        lm = LayerMapping(WorldBorder, world_shp, world_mapping,
                          transform=False, encoding='iso-8859-1')

        lm.save(strict=True, verbose=True)

        for country in WorldBorder.objects.all():
            gr = GeospatialReference(title=country.name, address=country.name,
                geometry=country.mpoly, point=Point(country.lon, country.lat),
                description='http://thematicmapping.org/')
            gr.save()
            print gr;

 # -*- coding: utf8 -*-
import os

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.contrib.gis.utils import LayerMapping
from django.db import transaction

import json

from base.models import WorldBorder, GeospatialReference
from studies.models import Speaker, Production, Study


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.get(id=1)
        diccio_f = open(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    'data', 'regionalismos.json')))
        diccio = json.load(diccio_f)


        with transaction.commit_on_success():
            st = Study (title = 'Regionalismos', user = user, 
                        authors = "Javier De la Rosa y Roberto Ulloa")
            st.save()
            self.create_location(user,name=u'Área del Río de la Plata')
            self.create_location(user,name=u'América')
            self.create_location(user,name=u'América Central')
            self.create_location(user,name=u'América Meridional')
            
            print "loading the objects into a dictionary..."
            grs = dict ((o.title, o) for o in GeospatialReference.objects.all())
            
            i=0
            for entry in diccio:
                #grs = GeospatialReference.objects.filter(title=entry['user'])
                #if len(grs) > 0:
                    #gr = grs[0]
                if entry['user'] in grs:
                    gr = grs[entry['user']]
                elif entry['user'] in [u'Ciudad de México', u'Guadalajara']:
                    gr = grs['Mexico']
                    #gr = GeospatialReference.objects.get(title='Mexico')
                else:
                    gr = grs['Spain']
                    #gr = GeospatialReference.objects.get(title='Spain')

                spkrs = Speaker.objects.filter(location=gr)
                if len(spkrs) > 0:
                    spkr = spkrs[0]
                else:
                    spkr = self.create_speaker(user, st ,gr, entry['user'])

                self.create_production(user, spkr, entry['word'], 
                          entry['ipa'], entry['rfe'], gr, entry['definition'])
                i+=1
                if i%100 == 0:
                    print str(i) + ' productions'

    def create_location(self, user, name=""):
        gr = GeospatialReference(
                    title=name,
                    address=name,
                    geometry=None,
                    point=Point(0, 0),
                    description='Generated through regionalisms loading',
                    user=user,
                )
        gr.save()
        return gr


    def create_speaker(self, user, st, loc, code):
        sp = Speaker(
                code = code,
                age = None,
                sex = None,
                education = None,
                location = loc,
                user = user
                )
        sp.save()
        sp.studies.add(st)
        return sp



    def create_production(self, user, spkr, word, ipa, rfe, loc, definition):
        prod = Production(
                user = user,
                speaker = spkr,
                word = word,
                language='es',
                approximate_word = word,
                lemma = word,
                ipa_transcription = ipa,
                rfe_transcription = rfe,
                location = loc,
                definition = definition
                )
        prod.save()
        return prod

# -*- coding: utf-8 -*-
from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from studies.models import Production
from studies.forms import ProductionAdminForm


class BaseAdmin(GuardedModelAdmin):
    user_can_access_owned_objects_only = True
    exclude = ('user', )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class StudyAdmin(BaseAdmin):
    pass


class LanguageAdmin(BaseAdmin):
    pass


class SpeakerAdmin(BaseAdmin):
    raw_id_fields = ("location", "studies")
    autocomplete_lookup_fields = {
        'fk': ['location'],
        'm2m': ['studies'],
    }


class ProductionAdmin(admin.ModelAdmin):

    class Media:
        js = ("admin/js/categories.js", 
              "js/functions11.js",
              "js/ipa.js",
              "js/n11n.js",
              "js/n11ndata-lite.js")
        css = {
                'all': ('css/style11.css','css/ipa.css'),
              }
    form = ProductionAdminForm


    readonly_fields = ('frequency', )
    exclude = ('user', 'frequency')
    search_fields = ('word', 'lemma', 'user__username',
                     'definition')
    list_display = ('word', 'lemma', 'category', 'features',
                    'frequency', 'user', 'date')
    lexical_fields = set()

    for categories in Production.CATEGORY_FIELDS.values():
        for value in categories:
            lexical_fields.add(value)
    lexical_fields = list(lexical_fields)
    fieldsets = (
        (None, {
            'fields': ('word', 'lemma')
        }),
        ('Transcriptions', {
            'fields': ('ipa_transcription', 'rfe_transcription', )
#                       'defsfe_transcription', 'sala_transcription',
#                       'worldbet_transcription', 'via_transcription')
        }),
        ('Encodings', {
            'fields': ('soundex_encoding', 'metaphone_encoding', )
#                       'nysiis_encoding',
#                       'codex_encoding')
        }),
        ('Grammar', {
            'classes': ('collapse',),
            'fields': ["category"] + lexical_fields,
        }),
    )
    list_filter = ('user', 'date', 'category')
    date_hierarchy = 'date'
    # list_editable = ('lemma', 'category', 'gender', 'number', 'person')
    save_as = True

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def features(self, obj, *args, **kwargs):
        return obj.get_features_display()
    features.allow_tags = True

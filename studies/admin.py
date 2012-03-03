# -*- coding: utf-8 -*-
from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from studies.models import Production, Language



class BaseAdmin(GuardedModelAdmin):
    user_can_access_owned_objects_only = True
    exclude = ('user', )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class StudyAdmin(BaseAdmin):
    pass


class LanguageAdmin(admin.TabularInline):
    model = Language
    exclude = ("user", )
    extra = 1
    raw_id_fields = ("immersion_location", )
    autocomplete_lookup_fields = {
        'fk': ['immersion_location'],
    }


class SpeakerAdmin(BaseAdmin):
    raw_id_fields = ("location", "studies")
    inlines = [LanguageAdmin]
    autocomplete_lookup_fields = {
        'fk': ['location'],
        'm2m': ['studies'],
    }

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.speaker = form.instance
            instance.save()
        formset.save_m2m()


class ProductionAdmin(GuardedModelAdmin):

    class Media:
        js = ("admin/js/categories.js", )

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
    raw_id_fields = ("speaker", "location")
    autocomplete_lookup_fields = {
        'fk': ['speaker', "location"],
    }
    fieldsets = (
        (None, {
            'fields': ('word', )
        }),
        ('Transcriptions', {
            'fields': ('ipa_transcription', 'rfe_transcription', )
#                       'defsfe_transcription', 'sala_transcription',
#                       'worldbet_transcription', 'via_transcription')
        }),
        ('Source', {
            'fields': ('speaker', 'location', 'lemma', )
#                       'nysiis_encoding',
#                       'codex_encoding')
        }),
        ('Encodings', {
            'classes': ('collapse',),
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

    def features(self, obj, *args, **kwargs):
        return obj.get_features_display()
    features.allow_tags = True

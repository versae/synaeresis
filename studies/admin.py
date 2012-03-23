# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from guardian.admin import GuardedModelAdmin

from base.admin import BaseAdmin
from studies.models import Production, Language


class LanguageAdmin(admin.TabularInline):
    model = Language
    exclude = ("user", )
    extra = 1
    raw_id_fields = ("immersion_location", )
    autocomplete_lookup_fields = {
        'fk': ['immersion_location'],
    }


class SpeakerAdmin(BaseAdmin):
    search_fields = ('code', 'location__title', 'location__address',
                     'studies__title')
    list_display = ('code', 'sex', 'age', 'location', 'studies_included')
    raw_id_fields = ("location", "studies")
    inlines = [LanguageAdmin]
    autocomplete_lookup_fields = {
        'fk': ['location'],
        'm2m': ['studies'],
    }
    save_on_top = True

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.speaker = form.instance
            instance.save()
        formset.save_m2m()

    def studies_included(self, obj):
        studies_titles = []
        for study in obj.studies.all():
            studies_titles.append(study.title)
        return mark_safe("</br>".join(studies_titles))
    studies_included.short_description = _(u"Studies")
    studies_included.allow_tags = True


class ProductionAdminForm(forms.ModelForm):

    class Meta:
        model = Production
        widgets = {
           'ipa_transcription': forms.TextInput(attrs={'class':
                                                       'vTextField ipakey'}),
           'rfe_transcription': forms.TextInput(attrs={'class':
                                                       'vTextField ipakey'})
       }


class ProductionAdmin(GuardedModelAdmin):

    class Media:
        js = ("admin/js/categories.js", 
              "js/n11n.js",
              "js/functions11.js",
              "js/n11ndata-lite.js",
              "js/ipa.js"
              )
        css = {
                'all': ('css/style11.css','css/ipa.css'),
              }
    form = ProductionAdminForm
    readonly_fields = ('frequency', )
    exclude = ('user', 'frequency')
    search_fields = ('word', 'lemma', 'user__username',
                     'definition')
    list_display = ('word', 'language',
                    'ipa_transcription', 'rfe_transcription',
                    'metaphone_encoding', 'soundex_encoding',
                    'speaker', 'location',
                    'lemma', 'category', 'features',
                    'date')
    lexical_fields = set()

    for categories in Production.CATEGORY_FIELDS.values():
        for value in categories:
            lexical_fields.add(value)
    lexical_fields = list(lexical_fields)
    raw_id_fields = ("speaker", "location", "media")
    autocomplete_lookup_fields = {
        'fk': ['speaker', "location", "media"],
    }
    fieldsets = (
        (None, {
            'fields': ('word', 'language')
        }),
        ('Transcriptions', {
            'fields': ('ipa_transcription', 'rfe_transcription',
                       'approximate_word')
        }),
        ('Source', {
            'fields': ('speaker', 'location', 'media', )
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
            'fields': ["lemma", "category"] + lexical_fields,
        }),
    )
    list_filter = ('date', 'category', 'ipa_transcription', 'rfe_transcription',
                   'metaphone_encoding', 'soundex_encoding', 'language')
    date_hierarchy = 'date'
    # list_editable = ('lemma', 'category', 'gender', 'number', 'person')
    save_as = True

    def features(self, obj, *args, **kwargs):
        return obj.get_features_display()
    features.allow_tags = True

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class StudyAdmin(BaseAdmin):
    search_fields = ('title', 'description', 'authors')
    list_display = ('title', 'description', 'authors')

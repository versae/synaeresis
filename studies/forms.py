# -*- coding: utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import gettext as _

from studies.models import Production, Study


class SearchForm(forms.Form):
    class Media:
        js = (
            "js/n11n.js",
            "js/n11ndata-lite.js",
            "js/functions11.js",
            "js/ipa.js"
        )
        css = {
            "all": (
                "css/style11.css",
                "css/ipa_search.css"
            )
        }

    q = forms.CharField(label=_("Word to search"), required=False,
                        max_length=100,
                        widget=forms.TextInput(attrs={'class':'ipakey output'}))

    def q_clean(self):
        q = super(SearchForm, self).q_clean()
        return q.strip()


class SearchOptionsForm(forms.Form):
    MATCH_CHOICES = (
        ("iexact", _("Exactly")),
        ("istartswith", _("The Beginning of")),
        ("iendswith", _("The End of")),
        ("iregex", _("As a Regular Expression")),
        ("icontains", _("Inside")),
    )
    match = forms.ChoiceField(label=_("Matching"), required=False,
                              choices=MATCH_CHOICES)
    WHERE_CHOICES = (
        ("word", _("Word")),
        ("ipa_transcription", _("IPA")),
        ("rfe_transcription", _("RFE")),
        ("soundex_encoding", _("Soundex")),
        ("metaphone_encoding", _("Metaphone")),
    )
    where = forms.ChoiceField(label=_("The"), required=False,
                              choices=WHERE_CHOICES)
    study = forms.ModelChoiceField(label=_("In"), queryset=Study.objects.all(),
                                   required=False, empty_label=_("Any study"))


class ProductionForm(forms.ModelForm):

    class Media:
        js = (
            "admin/js/categories.js",
            "js/chosen.jquery.min.js",
            "js/words.js",
        )
        css = {
            "all": ("css/chosen.css", ),
        }

    class Meta:
        model = Production
        exclude = ("word", "frequency", "lemma", "definition", "user", "eagle",
                   "notes", 'ipa_transcription', 'rfe_transcription',
                       'defsfe_transcription', 'sala_transcription',
                       'worldbet_transcription', 'via_transcription',
                       'soundex_encoding', 'metaphone_encoding',
                       'es_metaphone_encoding', 'nysiis_encoding',
                       'codex_encoding')
        widgets = {"category": forms.Select(attrs={"class": "category"})}
        for field in Production.CATEGORY_FIELDS.values():
            for value in field:
                widgets[value] = forms.RadioSelect(attrs={"class": "facet"})

    def __init__(self, *args, **kwargs):
        super(ProductionForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.fields.items():
            if field_name != "category":
                # field_value.choices[0] = ("", "None")
                # field_value.choices = field_value.choices[1:]
                pass
            else:
                field_value.required = False

    def get_data(self):
        cleaned_data = self.cleaned_data
        if "category" in cleaned_data:
            if cleaned_data["category"]:
                data = {"category": cleaned_data["category"]}
            else:
                data = {}
            if cleaned_data["category"] in LexicalEntry.CATEGORY_FIELDS:
                for field in LexicalEntry.CATEGORY_FIELDS[cleaned_data["category"]]:
                    if field in cleaned_data and cleaned_data[field]:
                        data[field] = cleaned_data[field]
            return data
        else:
            return cleaned_data

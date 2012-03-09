# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext as _

from studies.models import Production


class SearchForm(forms.Form):
    q = forms.CharField(label=_("Search"), required=False,
                        max_length=100)

    def q_clean(self):
        q = super(SearchForm, self).q_clean()
        return q.strip()


class SearchOptionsForm(forms.Form):
    MATCH_CHOICES = (
        ("iexact", _("Exactly the Word")),
        ("istartswith", _("The Beginning of the Word")),
        ("iendswith", _("The End of the Word")),
        ("iregex", _("As a Regular Expression")),
        ("icontains", _("Inside the Word")),
    )
    match = forms.ChoiceField(label=_("Matching"), required=False,
                              choices=MATCH_CHOICES)
    WHERE_CHOICES = (
        ("word", _("Word")),
        ("ipa_transcription", _("IPA")),
        ("rfe_transcription", _("RFE")),
        ("soundex", _("Soundex")),
        ("metaphone", _("Metaphone")),
    )
    where = forms.ChoiceField(label=_("In"), required=False,
                              choices=WHERE_CHOICES)

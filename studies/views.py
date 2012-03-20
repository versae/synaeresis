# -*- coding: utf-8 -*-
import types
from json import dumps
from urllib import urlencode

from django.conf import settings
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import connection, DatabaseError
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from base.models import GeospatialReference
from base.utils import json_encode
from studies.forms import SearchForm, SearchOptionsForm
from studies.models import Production


def mapper(request):
    data = request.GET.copy()
    search_form = SearchForm(label_suffix="", data=data)
    search_options_form = SearchOptionsForm(data=data)
    q = None
    entries = []
    query_time = 0.0
    start_list = 1
    regexp_error = False
    if (request.is_ajax() or settings.DEBUG) and data:
        if (search_form.is_valid() and search_options_form.is_valid()):
            q = search_form.cleaned_data["q"]
            options = search_options_form.cleaned_data
            if q:
                to_search = options["where"]
                key = "productions__%s__%s" \
                      % (to_search, options.get("match") or "iexact")
                params = {key: q}
                if data["study"]:
                    params.update({
                        "productions__speaker__studies__id": data["study"],
                    })
                references = GeospatialReference.objects.filter(**params)
                annotated_entries = references.distinct().annotate(
                    num_productions=Count('productions')
                )
                total_productions = 0
                for e in annotated_entries.values():
                    entry = dict(e)
                    entry["point"] = entry["point"].wkt
                    entries.append(entry)
                    total_productions += entry["num_productions"]
                result = {
                    "id": data["id"],
                    "total": total_productions,
                }
                if entries:
                    result.update({
                        "places": entries
                    })
                return HttpResponse(json_encode(result),
                                    status=200, mimetype='application/json')
                # Grouping by not documented API
                # entry_list.query.group_by = ['lemma']
                paginator = Paginator(entry_list, 15)
                # Make sure page request is an int. If not, deliver first page.
                try:
                    page = int(request.GET.get('page', '1'))
                except ValueError:
                    page = 1
                # If page request (9999) is out of range, deliver last page of results.
                try:
                    entries = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    entries = paginator.page(paginator.num_pages)
                except DatabaseError:
                    entry_list = Production.objects.none()
                    paginator = Paginator(entry_list, 15)
                    entries = paginator.page(1)
                    regexp_error = True
                if connection.queries:
                    query_time = connection.queries[-1]["time"]
                start_list = ((entries.number - 1) * entries.paginator.per_page) + 1
    data.pop("page", None)
    # HACK: Avoid crash on unicode characters in urlencode
    # Taken from: http://evanculver.com/2009/10/12/url-encoding-weird-unicode-characters-in-pythondjango/
    data = dict([(k, v.encode('utf-8') if type(v) is types.UnicodeType else v)
                 for (k,v) in data.items()])
    url_path = urlencode(data)
    return render_to_response('map.html',
                              {"search_form": search_form,
                               "search_options_form": search_options_form,
                               "entries": entries,
                               "query_time": query_time,
                               "start_list": start_list,
                               "url_path": url_path,
                               "regexp_error": regexp_error,
                               "q": q},
                              context_instance=RequestContext(request))


def grid(request):
    return render_to_response('grid.html',
                              {},
                              context_instance=RequestContext(request))


def ipa_keyboard(request, input_id=None):
    input_id = input_id or request.GET.get("input_id", "output")
    return render_to_response('ipa.html', {"input_id": input_id},
                              context_instance=RequestContext(request))


def search(request):
    data = request.GET.copy()
    search_form = SearchForm(label_suffix="", data=data)
    search_options_form = SearchOptionsForm(data=data)
    entry_form = ProductionForm()
    q = None
    entries = []
    query_time = 0.0
    start_list = 1
    regexp_error = False
    if data:
        entry_form = ProductionForm(data=data)
        if (search_form.is_valid() and search_options_form.is_valid()
            and entry_form.is_valid()):
            q = search_form.cleaned_data["q"]
            options = search_options_form.cleaned_data
            params = entry_form.get_data()
            if q:
                to_search = "word"
                if options["in_lemma"]:
                    to_search = "lemma"
                key = "%s__%s" % (to_search, options.get("match") or "iexact")
                params[key] = q
                entry_list = Production.objects.filter(**params)
                # Grouping by not documented API
                # entry_list.query.group_by = ['lemma']
                paginator = Paginator(entry_list, 15)
                # Make sure page request is an int. If not, deliver first page.
                try:
                    page = int(request.GET.get('page', '1'))
                except ValueError:
                    page = 1
                # If page request (9999) is out of range, deliver last page of results.
                try:
                    entries = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    entries = paginator.page(paginator.num_pages)
                except DatabaseError:
                    entry_list = Production.objects.none()
                    paginator = Paginator(entry_list, 15)
                    entries = paginator.page(1)
                    regexp_error = True
                if connection.queries:
                    query_time = connection.queries[-1]["time"]
                start_list = ((entries.number - 1) * entries.paginator.per_page) + 1
    data.pop("page", None)
    # HACK: Avoid crash on unicode characters in urlencode
    # Taken from: http://evanculver.com/2009/10/12/url-encoding-weird-unicode-characters-in-pythondjango/
    data = dict([(k, v.encode('utf-8') if type(v) is types.UnicodeType else v)
                 for (k,v) in data.items()])
    url_path = urlencode(data)
    return render_to_response('search.html',
                              {"search_form": search_form,
                               "search_options_form": search_options_form,
                               "entry_form": entry_form,
                               "entries": entries,
                               "query_time": query_time,
                               "start_list": start_list,
                               "url_path": url_path,
                               "regexp_error": regexp_error,
                               "q": q},
                              context_instance=RequestContext(request))

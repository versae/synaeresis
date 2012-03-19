# -*- coding: utf-8 -*-
# Copied and modified from https://github.com/versae/neo4j-rest-client/
import datetime
import decimal
import json
import re

from django.db.models.query import QuerySet
from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads, JSONEncoder


# Proleptic Gregorian dates and strftime before 1900 « Python recipes
# ActiveState Code: http://bit.ly/9t0JKb via @addthis
def findall(text, substr):
    # Also finds overlaps
    sites = []
    i = 0
    while 1:
        j = text.find(substr, i)
        if j == -1:
            break
        sites.append(j)
        i = j + 1
    return sites


# Every 28 years the calendar repeats, except through century leap
# years where it's 6 years.  But only if you're using the Gregorian
# calendar.  ;)
def strftime(dt, fmt):
    _illegal_s = re.compile(r"((^|[^%])(%%)*%s)")
    if _illegal_s.search(fmt):
        raise TypeError("This strftime implementation does not handle %s")
    if dt.year > 1900:
        return dt.strftime(fmt)
    year = dt.year
    # For every non-leap year century, advance by
    # 6 years to get into the 28-year repeat cycle
    delta = 2000 - year
    off = 6 * (delta // 100 + delta // 400)
    year = year + off
    # Move to around the year 2000
    year = year + ((2000 - year) // 28) * 28
    timetuple = dt.timetuple()
    s1 = time.strftime(fmt, (year,) + timetuple[1:])
    sites1 = findall(s1, str(year))
    s2 = time.strftime(fmt, (year + 28,) + timetuple[1:])
    sites2 = findall(s2, str(year + 28))
    sites = []
    for site in sites1:
        if site in sites2:
            sites.append(site)
    s = s1
    syear = "%4d" % (dt.year, )
    for site in sites:
        s = s[:site] + syear + s[site + 4:]
    return s


def json_encode(data, ensure_ascii=False):

    def _any(data):
        DATE_FORMAT = "%Y-%m-%d"
        TIME_FORMAT = "%H:%M:%S"
        ret = None
        if isinstance(data, (list, tuple)):
            ret = _list(data)
        elif isinstance(data, dict):
            ret = _dict(data)
        elif isinstance(data, decimal.Decimal):
            ret = str(data)
        elif isinstance(data, datetime.datetime):
            ret = strftime(data, "%s %s" % (DATE_FORMAT, TIME_FORMAT))
        elif isinstance(data, datetime.date):
            ret = strftime(data, DATE_FORMAT)
        elif isinstance(data, datetime.time):
            ret = data.strftime(TIME_FORMAT)
        elif isinstance(data, QuerySet):
            ret = loads(serialize('json', data))
        else:
            ret = data
        return ret

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        ret = {}
        for k, v in data.items():
            ret[k] = _any(v)
        return ret
    ret = _any(data)
    return json.dumps(ret, ensure_ascii=ensure_ascii)

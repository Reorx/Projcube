#coding=utf-8

from django import template
from django.utils.encoding import force_unicode
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def to01(num):
    if num%2 == 0:
        return 0
    return 1

@register.filter
@stringfilter
def numRise(value, r):
    return str(int(value) + int(r))

@register.filter
@stringfilter
def numFall(value, r):
    return str(int(value) - int(r))


# before
@register.filter
@stringfilter
def truncatefilter(value, num):
    try:
        length = int(num)
    except ValeError:
        return value
    unicode_value = force_unicode(value)
    if length < unicode_value.__len__():
        value = unicode_value[:length] + '...'
    else:
        value = unicode_value
    return value
truncatefilter.is_safe = True

@register.filter
def compare_by_now(dt):
    import datetime
    from utils.timer import get_time_delta
    return get_time_delta(dt, datetime.datetime.now())
compare_by_now.is_safe = True

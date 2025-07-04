# templatetags/formatters.py
from django import template
import locale
locale.setlocale(locale.LC_ALL, '')

register = template.Library()

@register.filter
def rupiah(value):
    try:
        return "Rp {:,}".format(int(value)).replace(",", ".")
    except:
        return value

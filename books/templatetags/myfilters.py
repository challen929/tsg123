from django import template
import datetime
import decimal
register = template.Library()


@register.filter(name="div")
def div(arg, arg2):
    return round(arg / arg2 * 100)


@register.filter(name="decimal_places")
def decimal_places(arg, arg2):
    return format(decimal.Decimal(arg), ".{}f".format(arg2))

from django import template
import math

register = template.Library()


@register.filter
def floor(value):
    """
    Takes a float value and returns the value rounded down to the nearest whole number.
    """
    return math.floor(value)


@register.filter
def full_stars(value):
    """
    Takes a float value and returns a range object up to the nearest whole number.
    This is intended to be used for displaying full stars in a star rating system.
    """
    return range(math.floor(value))


@register.filter
def half_star(value):
    """
    Takes a float value and returns True if the decimal part of the number is equal to or greater than 0.5.
    This is intended to be used for displaying a half star in a star rating system.
    """
    return math.modf(value)[0] >= 0.5


@register.filter
def round_half(value):
    """
    Takes a float value and rounds it to the nearest half number (0.5 increment).
    """
    return round(value * 2) / 2


@register.filter
def subtract(value, arg):
    return value - arg

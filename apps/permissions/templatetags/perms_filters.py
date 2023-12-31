from django import template

register = template.Library()


@register.filter
def get_perm(dictionary, key):
    return dictionary.get(key)

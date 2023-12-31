from django import template
import os

register = template.Library()


@register.filter
def starts_with(value, prefix):
    """
    Custom template filter to check if a given string starts with a specific prefix.

    Parameters:
        value (str): The input string to check.
        prefix (str): The prefix string to check for at the beginning of the input string.

    Returns:
        bool: Returns True if the input string starts with the specified prefix, otherwise False.
    """
    return value.startswith(prefix)


@register.filter
def extension(value):
    return os.path.splitext(value.name)[1][1:]

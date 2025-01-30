from django import template

register = template.Library()

@register.filter
def spaces_to_underscores(value):
    return value.lower().replace(' ', '_')

@register.filter
def format_price(value):
    return "{:.2f}".format(value)

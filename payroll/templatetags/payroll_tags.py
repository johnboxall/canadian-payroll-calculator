from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter(name='sum')
def sum_(iterable, attribute=None):
    if attribute is not None:
        total = 0
        for i in iter(iterable):
            attr = getattr(i, attribute)
            
            if callable(attr):
                total += attr()
            else:
                total += attr
        return total
    return sum(iterable)
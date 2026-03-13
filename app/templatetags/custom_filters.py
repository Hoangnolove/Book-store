from django import template

register = template.Library()

@register.filter
def batch(iterable, size):
    
    l = list(iterable)
    for i in range(0, len(l), size):
        yield l[i:i + size]
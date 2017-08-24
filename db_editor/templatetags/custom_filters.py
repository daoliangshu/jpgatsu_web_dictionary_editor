from django import template

register = template.Library()

print('LOAD_CUSTOM_FILTERS')


@register.filter(name='get_key_value')
def get_key_value(d, key):
    for k, v in d:
        if k == key:
            return str(v)
    return ''


@register.filter(name='times')
def times(number):
    return range(number)

from django import template

register=template.Library()
@register.filter()
def myfilter(data):
    if len(data)>4:
        return data[:4]
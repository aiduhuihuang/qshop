from django import template

register=template.Library()
@register.filter
def myfilter(num1,num2):
    s=round(float(num1)+float(num2),2)
    print(s)
    return s
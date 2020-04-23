from django import template
register = template.Library()

@register.filter
def div(value, div):
    if value==0 or div==0 or value == 0.00 or div== 0.00:
        return 0
    else:
        return round((value / div) * 100, 2)

@register.filter
def mul(value, div):
    return round((value * div) , 2)
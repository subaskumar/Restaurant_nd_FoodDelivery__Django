from django import template
from myRestaurant.models import MenuItem,Catagory
from django.db.models import Q


register = template.Library()

@register.simple_tag
def Special_items():
    items = MenuItem.objects.filter(Q(catagory__name__iexact = 'Special') | Q(catagory__name__iexact = 'Lunch'))
    return items

@register.simple_tag
def Breakfast_items():
    items = MenuItem.objects.filter(catagory__name__iexact = 'Breakfast')
    return items

@register.simple_tag
def Dinner_items():
    items = MenuItem.objects.filter(catagory__name__iexact = 'Dinner')
    return items
  
@register.simple_tag
def Lunch_items():
    items = MenuItem.objects.filter(catagory__name__iexact = 'Coffee_Drinks')
    return items

@register.simple_tag
def All_items():
    items = MenuItem.objects.all()
    return items

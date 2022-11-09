from django import template
#from django.db.models import Sum
#from django.urls import reverse

from ecom import settings
#from product.models import Category

register = template.Library()




""" @register.simple_tag
def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count """

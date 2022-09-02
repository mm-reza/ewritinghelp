#pylint: disable=W0614
from django.contrib import admin
from product.models import Product
from order.models import *

# Register your models here.

"""

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'price', 'amount', 'user']
    list_filter = ['user']
    readonly_fields = ('img_tag',)
    


class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product','price','quantity','amount')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','code', 'files', 'first_name', 'last_name','phone','phone_company', 'phone_location','city','total', 'account', 'status', 'create_at', 'update_at']
    list_filter = ['status']
    readonly_fields = ('user','address','city','country','phone', 'first_name','ip', 'last_name','phone','city','total')
    can_delete = False
    inlines = [OrderProductline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product','price','quantity','amount']
    list_filter = ['user']

admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)

"""




##### File models here #####

    
class FOrderAdmin(admin.ModelAdmin):
    list_display = ['id','code', 'files', 'first_name', 'phone', 'status', 'create_at', 'update_at', 'reports']
    list_filter = ['status']
    readonly_fields = ('phone', 'ip', )
    can_delete = False
    
admin.site.register(FOrder, FOrderAdmin)






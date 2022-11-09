#pylint: disable=W0614
from django.contrib import admin
from order.models import *

##### File models here #####

    
class FOrderAdmin(admin.ModelAdmin):
    list_display = ['id','code', 'files', 'first_name', 'phone', 'status', 'create_at', 'update_at', 'reports']
    list_filter = ['status']
    readonly_fields = ('phone', 'ip', )
    can_delete = False
    
admin.site.register(FOrder, FOrderAdmin)






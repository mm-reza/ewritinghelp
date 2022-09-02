from django.contrib import admin

# Register your models here.
from user.models import UserProfile, Reply


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'email_confirmed', 'create_at','email', 'address', 'phone','city','country','image_tag']

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['order', 'subject','reply', 'status', 'create_at', 'image_tag',]
    list_filter = ['status',]
    readonly_fields = ('ip',)
    

admin.site.register(Reply,ReplyAdmin)
admin.site.register(UserProfile,UserProfileAdmin)


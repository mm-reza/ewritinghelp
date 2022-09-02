# pylint: disable=W0614
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from product import models
from product.models import *
import admin_thumbnails

"""
class CategoryInline(admin.TabularInline):
	model = Category
	extra = 1
	show_change_link = True
	prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
	list_display = ['title', 'status', 'parent', 'image_tag']
	list_filter = ['status']

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count', 'status', 'parent', 'image_tag')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 3

class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True

@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
	list_display = ['title','image_tag', 'image','image_thumbnail']
		
class ProductAdmin(admin.ModelAdmin):
	list_display = ['title','category', 'image_tag', 'id', 'amount', 'price']
	list_filter = ['title']
	readonly_fields = ('image_tag',)
	prepopulated_fields = {'slug': ('title',)}
	inlines = [ProductImageInline, ProductVariantsInline]
	
class ColorAdmin(admin.ModelAdmin):
	list_display = ['name','code','color_tag']

class SizeAdmin(admin.ModelAdmin):
	list_display = ['name','code']


class VariantsAdmin(admin.ModelAdmin):
	list_display = ['title','product','color','size','price','quantity','image_tag']
	
	
# Register your models here.
admin.site.register(Category, CategoryAdmin2)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Variants,VariantsAdmin) 

"""

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment', 'status', 'create_at', 'rate', 'product', 'image_tag']
    list_filter = ['status']
    readonly_fields = ('subject','comment','ip','user','product','id')

admin.site.register(Comment,CommentAdmin)



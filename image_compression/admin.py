from django.contrib import admin
from .models import CompressImage
from django.utils.html import format_html

class CompressImageAdmin(admin.ModelAdmin):

    def thumbnail(self, obj):
        return format_html('<img src="{}" width="40" height="40">',obj.compressed_image.url)
    
    def org_img_size(self, obj):
        size_in_mb = obj.original_image.size / (1024 * 1024)
        if size_in_mb > 1:
            return format_html("{} MB",round(size_in_mb,2))
        else:
            return format_html("{} KB",round(obj.original_image.size/1024,2))
    def comp_img_size(self, obj):
        size_in_mb = obj.compressed_image.size / (1024 * 1024)
        if size_in_mb > 1:
            return format_html("{} MB",round(size_in_mb,2))
        else:
            return format_html("{} KB",round(obj.compressed_image.size/1024,2))
    list_display = ('user','thumbnail' ,'org_img_size','comp_img_size', 'compressed_at')
    
# Register your models here.
admin.site.register(CompressImage, CompressImageAdmin)
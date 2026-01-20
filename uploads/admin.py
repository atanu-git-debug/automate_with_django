from django.contrib import admin

from uploads.models import Upload




class uploadAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'uploaded_at')

# Register your models here.

admin.site.register(Upload,uploadAdmin)
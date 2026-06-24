from django.contrib import admin  
from .models import Advertisement  

class AdvertisementAdmin(admin.ModelAdmin):  
    list_display = ('title', 'created_at')  
    search_fields = ('title',)  

admin.site.register(Advertisement, AdvertisementAdmin)
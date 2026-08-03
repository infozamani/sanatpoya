from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Advertisement

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'title', 
        'image_preview', 
        'url', 
        'created_at',
        'expiry_date',
        'is_active',  # ✅ این خط را اضافه کنید
        'is_active_display',
        'is_expired_display',
        'view_count_display'
    )
    
    search_fields = ('title', 'description', 'url')
    list_filter = ('created_at', 'is_active', 'expiry_date')
    list_editable = ('is_active',)  # ✅ حالا درست کار می‌کند
    ordering = ('-created_at',)
    list_per_page = 20
    readonly_fields = ('created_at', 'image_preview')
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'description', 'image_name', 'url')
        }),
        ('تنظیمات زمان', {
            'fields': ('expiry_date', 'is_active'),
            'classes': ('wide',),
        }),
        ('آمار', {
            'fields': ('views_count', 'created_at'),
            'classes': ('collapse',),
        }),
    )
    
    def image_preview(self, obj):
        if obj.image_name and hasattr(obj.image_name, 'url'):
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 8px; object-fit: cover;" />',
                obj.image_name.url
            )
        return format_html(
            '<span style="color: #999; font-size: 12px;">بدون تصویر</span>'
        )
    image_preview.short_description = 'تصویر'
    
    def is_active_display(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background: #10b981; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">✓ فعال</span>'
            )
        return format_html(
            '<span style="background: #ef4444; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">✗ غیرفعال</span>'
        )
    is_active_display.short_description = 'وضعیت'
    
    def is_expired_display(self, obj):
        if obj.is_expired():
            return format_html(
                '<span style="background: #ef4444; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">⛔ منقضی</span>'
            )
        return format_html(
            '<span style="background: #10b981; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">✅ معتبر</span>'
        )
    is_expired_display.short_description = 'انقضا'
    
    def view_count_display(self, obj):
        return format_html(
            '<span style="background: #3b82f6; color: white; padding: 2px 10px; border-radius: 12px; font-size: 13px;">{} بازدید</span>',
            obj.views_count
        )
    view_count_display.short_description = 'بازدید'

admin.site.register(Advertisement, AdvertisementAdmin)
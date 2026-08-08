# teams/admin.py
from django.contrib import admin
from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'experience_years', 'is_featured', 'is_active', 'order')
    list_filter = ('is_featured', 'is_active', 'role')
    search_fields = ('name', 'role', 'email', 'bio')
    list_editable = ('order', 'is_featured', 'is_active')
    
    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': ('name', 'role', 'bio', 'photo', 'experience_years')
        }),
        ('اطلاعات تماس', {
            'fields': ('email', 'phone')
        }),
        ('اطلاعات حرفه‌ای', {
            'fields': ('credentials', 'skills')
        }),
        ('شبکه‌های اجتماعی', {
            'fields': ('linkedin', 'twitter', 'facebook', 'instagram')
        }),
        ('تنظیمات نمایش', {
            'fields': ('order', 'is_featured', 'is_active')
        }),
    )
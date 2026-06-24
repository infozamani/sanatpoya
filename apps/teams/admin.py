from django.contrib import admin
from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'experience_years', 'is_featured', 'is_active', 'order')
    list_filter = ('is_featured', 'is_active', 'role', 'created_at')
    search_fields = ('name', 'role', 'email', 'bio')
    list_editable = ('order', 'is_featured', 'is_active')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'role', 'bio', 'photo', 'experience_years')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Professional Information', {
            'fields': ('credentials', 'skills')
        }),
        ('Social Media', {
            'fields': ('linkedin', 'twitter', 'facebook', 'instagram')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_featured', 'is_active')
        }),
    )
    
    def display_credentials(self, obj):
        """نمایش مدارک در لیست ادمین"""
        creds = obj.get_credentials_list()
        if creds:
            return ', '.join(creds[:3])
        return '-'
    display_credentials.short_description = 'Credentials'
    
    def display_skills(self, obj):
        """نمایش مهارت‌ها در لیست ادمین"""
        skills = obj.get_skills_list()
        if skills:
            return ', '.join(skills[:3])
        return '-'
    display_skills.short_description = 'Skills'
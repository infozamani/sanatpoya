from django.contrib import admin  
from .models import Ticket, TicketReply   

class TicketReplyInline(admin.TabularInline):
    model = TicketReply
    extra = 1

@admin.register(Ticket)  
class TicketAdmin(admin.ModelAdmin):  
    list_display = ['user', 'title', 'status', 'created_at', 'has_replies']  
    search_fields = ['title', 'description']  
    list_filter = ('status',  )   
    inlines = [TicketReplyInline,]
    def has_replies(self, obj):  
        return obj.replies.exists()  
    has_replies.boolean = True  
    has_replies.short_description = 'پاسخ‌ها'  

class NoReplyTicketFilter(admin.SimpleListFilter):  
    title = 'بدون پاسخ'  
    parameter_name = 'no_reply'  

    def lookups(self, request, model_admin):  
        return (  
            ('yes', 'بدون پاسخ'),  
            ('no', 'با پاسخ'),  
        )  

    def queryset(self, request, queryset):  
        if self.value() == 'yes':  
            return queryset.exclude(replies__isnull=False)  # تیکت‌هایی که جواب دارند را حذف می‌کند  
        if self.value() == 'no':  
            return queryset.filter(replies__isnull=False)  # فقط تیکت‌هایی که پاسخ دارند  
        return queryset  
 
@admin.register(TicketReply)  
class TicketReplyAdmin(admin.ModelAdmin):  
    list_display = ['ticket', 'user', 'created_at', 'is_active']  
    search_fields = ['ticket__title', 'message']


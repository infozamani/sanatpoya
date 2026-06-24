from django.contrib import admin
from .models import Slider,AboutUs,Post

def de_active_product(modeladmin,request,queryset):
    res = queryset.update(is_active = False)
    message = f'تعداد{res}کالا غیر فعال شد'
    modeladmin.message_user(request,message)
#-----------------------------------------------------------------------   
def active_product(modeladmin,request,queryset):
    res = queryset.update(is_active = True)
    message = f'تعداد{res}کالا غیر فعال شد'
    modeladmin.message_user(request,message)
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('image_slide','slider_title1','link','is_active','register_date')    
    list_filter = ('slider_title1',)
    search_fields = ('slider_title1',)
    ordering = ('update_date',)
    readonly_fields = ('image_slide',)
    
@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = (  'about_title','image_title','is_active','register_date')    
    list_filter = ('about_title',)
    search_fields = ('about_title',)
    ordering = ('update_date',)
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name','title','descriptions','email','is_active' )  
    actions = [de_active_product,active_product]
    list_editable = ['is_active']
    
    #--------------------------------------------
    ##  create pertion برای فارسی کردن سر ستونها
    de_active_product.short_description = 'غیر فعال کردن کالا های انتخاب شده'
    active_product.short_description = ' فعال کردن کالا های انتخاب شده'
    
 
    
    
    
    
    
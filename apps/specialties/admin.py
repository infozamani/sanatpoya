from django.contrib import admin
from .models import Identity,Ability,Services,FieldWork,ExpertGallery, ExpertiseGroup,Expert, FeatureExpertValue,ExpertFeature,Feature,FeatureExpertValue
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q  
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description,order_field ##pip install django-admin-decorators
from django_admin_listfilter_dropdown.filters import  DropdownFilter###pip install django-admin-list-filter-dropdownدر ستینگ هم اضافه شود

 
#---------------------------------------------------
#create class for Column group_parent and persion and updete
#-------------------------
##actions
def de_active_product_group(modeladmin,request,queryset):
    res = queryset.update(is_active = False)
    message = f'تعداد گروه {res}کالا غیر فعال شد'
    modeladmin.message_user(request,message)
    
def active_product_group(modeladmin,request,queryset):
    res = queryset.update(is_active = True)
    message = f'تعدادگروه{res}کالا غیر فعال شد'
    modeladmin.message_user(request,message)
 #-------------------------
## create export_file json
def export_json(modeladmin,request,queryset):
    response = HttpResponse(content_type = 'application/json')
    serializers.serialize("json",queryset,stream = response)
    return response
 
#---------------------------------------------------
@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    list_dialects = ('identity_name',)
    list_filter = ('identity_name',)
    search_fields = ('identity_name',)
    ordering = ('identity_name',)
#---------------------------------------------------
@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_dialects = ('ability_name',)
    list_filter = ('ability_name',)
    search_fields = ('ability_name',)
    ordering = ('ability_name',)
#---------------------------------------------------
@admin.register(FieldWork)
class FieldWorkAdmin(admin.ModelAdmin):
    list_dialects = ('fieldwork_name',)
    list_filter = ('fieldwork_name',)
    search_fields = ('fieldwork_name',)
    ordering = ('fieldwork_name',)
#---------------------------------------------------
@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_dialects = ('service_name',)
    list_filter = ('service_name',)
    search_fields = ('service_name',)
    ordering = ('service_name',)
#---------------------------------------------------
##craete filterGroup
class GroupFilter(SimpleListFilter):
    title = 'گروه تخصص ها '
    parameter_name = 'group'
    
    def lookups(self, request, model_admin):
        sub_groups = ExpertiseGroup.objects.filter(~Q(group_parent = None))
        groups = set([item.group_parent for item in sub_groups])
        return [(item.id, item.group_title) for item in groups]
    def queryset(self, request, queryset) :
        if self.value()!= None:
            return queryset.filter(Q(group_parent = self.value()))
        return queryset
#-----------------------------------------------------------------------
## create FeatuerInstance product
class ProductFeatureInstanceAdmin(admin.TabularInline):
    model = ExpertFeature
    extra = 3
#-------------------------
## create sub_group    
class ExpertiseGroupInstanceInlineAdmin(admin.TabularInline):
    model = ExpertiseGroup
    extra = 1
# #---------------------------------------------------

@admin.register(ExpertiseGroup)
class ExpertiseGroupAdmin(admin.ModelAdmin):
    list_display = ('group_title','is_active','group_parent','slug','register_date','update_date',)
    list_filter = (GroupFilter,('group_parent',DropdownFilter), 'is_active')
    search_fields = ('group_title',)
    ordering = ('group_title','group_parent')
    inlines = [ExpertiseGroupInstanceInlineAdmin]
    actions = [de_active_product_group,active_product_group,export_json]
    list_editable = ['is_active']
    #---------------------------------------------
    ##create Column products_of_groups
    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
       qs = super(ExpertiseGroupAdmin,self).get_queryset(*args, **kwargs)
       qs = qs.annotate(sub_group = Count('groups_parent'))
       qs = qs.annotate(product_of_group = Count('expertises_of_group'))
       return qs
    def count_sun_group(self, object):
        return object.sub_group
    
    @short_description('تعداد کالاهای گروه')
    @order_field('product_of_group')
    def count_product_of_group(self, object):
        return object.expertises_of_group
#-----------------------------------------------------------------------
def de_active_product(modeladmin,request,queryset):
    res = queryset.update(is_active = False)
    message = f'تعداد{res}کالا غیر فعال شد'
    modeladmin.message_user(request,message)
#-----------------------------------------------------------------------   
def active_product(modeladmin,request,queryset):
    res = queryset.update(is_active = True)
    message = f'تعداد{res}کالا غیر فعال شد'
    modeladmin.message_user(request,message)
#-----------------------------
    def count_sun_group(self, object):
        return object.sub_group
# #-------------------------
# ##  create pertion
    count_sun_group.short_description = 'تعداد زیر گروه ها'
    # count_product_of_group.short_description = 'تعداد کالا ها'
    de_active_product_group.short_description = 'غیر فعال کردن کالا های انتخاب شده'
    active_product_group.short_description = ' فعال کردن کالا های انتخاب شده'
    export_json.short_description = 'خروجی جیسونی از گروه انتخاب شده '
#-----------------------------------------------------------------------
## create FeatuerInstance product
class ProductFeatureInstanceAdmin(admin.TabularInline):
    model = ExpertFeature
    extra = 3
        #==================================================
    class Media:
        css = {
            'all' :('css/admin_style.css',)
        }
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'js/admin_script.js',)
#-----------------------------------------------------------------------
## create save Similar feature value product
class FeatureValueInlineAdmin(admin.TabularInline):
    model = FeatureExpertValue
    extra = 3
# #-----------------------------------------------------------------------
# ## create Featureadmin
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name','display_groups',  'display_freature_value')
    list_filter = ('feature_name',)
    search_fields = ('feature_name',)
    ordering = ('feature_name',)
    inlines = [FeatureValueInlineAdmin,]
 
     #--------------------------------------------
    ##create def formfield_for_manytomany(self, db_field, request, **kwargs):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'expertise_group':
            kwargs['queryset'] = ExpertiseGroup.objects.filter(~Q(group_parent = None))
        return super().formfield_for_manytomany(db_field,request,**kwargs)
     #--------------------------------------------
    def display_groups(self,obj):
        return ','.join([group.group_title for group in obj.expert_group.all()])
     #--------------------------------------------
    def display_freature_value(self,obj):
        return ', '.join([feature_value.value_title for feature_value in obj.feature_value.all()])
    display_groups.short_description = 'گروه ها دارای این ویژگی'
    display_freature_value.short_description = 'مقادیر ممکن برای این ویژگی' 
#----------------------------------------------------------------
## create FeatureValuAadmin
@admin.register(FeatureExpertValue)
class FeatureValueAdmin(admin.ModelAdmin):
    list_display =('value_title','feature')
    
    fieldsets = ((None,{'fields':('feature','value_title',)}),)
#-----------------------------------------------------------------------
## create save Similar gallery product
class ProductProductGalleryInlineAdmin(admin.TabularInline):
    model = ExpertGallery
    extra = 3
#----------------

#-----------------------------------------------------------------------
@admin.register(Expert  )
class ExpertAdmin(admin.ModelAdmin):
    list_display =  ('expert_user','is_active','identity','service' ,'fieldwork','ability' ,'update_date','slug',)
    list_filter = ('identity' ,'ability','fieldwork' ,'service')
    list_filter = (('identity__identity_name' ),('service__service_name' ) ,('ability__ability_name' ),('fieldwork__fieldwork_name' ),('expertise_group__group_title' ),)
    search_fields = ('expert_user',)
    ordering = ('update_date','expert_user')
    actions = [de_active_product,active_product,]
    inlines = [ProductFeatureInstanceAdmin,ProductProductGalleryInlineAdmin]
    list_editable = ['is_active']
    de_active_product.short_description = 'غیر فعال کردن کالا های انتخاب شده'
    active_product.short_description = ' فعال کردن کالا های انتخاب شده'
# #----------------------------
# # ##create Column for any object or fields
    def display_product_groups(self,obj):
        return ', '.join([group.group_title for group in obj.expertise_group.all()])
    display_product_groups.short_description = 'گروه کالا'

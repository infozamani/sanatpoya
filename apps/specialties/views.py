from django.shortcuts import render,get_object_or_404,redirect
from .models import   Expert,Ability,Services,FieldWork, ExpertiseGroup,Identity, FeatureExpertValue
from django.db.models import Q,Count,Min,Max
from django.views import View
# from .filters import ProductFilter
from django.core.paginator import Paginator
# from .compare import CompareProduct
from django.http import JsonResponse  
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import Customer
from apps.comment_scoring_favorites.models import ScoringExpert
from .form import ExpertForm
from django.db.models import Sum,Avg


#--------------------------------------------------------------------
## create class list brands  products for filter فdلتر کالاهای براساس برند
def get_identitys(request,*args, **kwargs):
    expert_group = get_object_or_404(ExpertiseGroup,slug=kwargs['slug'])
    identity_list_id = expert_group.expertises_of_group.filter(is_active = True).values('identity_id')
    identitys = Identity.objects.filter(pk__in=identity_list_id)\
                            .annotate(count = Count('identity'))\
                            .filter(~Q(count=0))\
                            .order_by('-count')
   
    return render(request,'specialtie_app/partials/identitys_filter.html',{'identitys':identitys})
#--------------------------------------------------------------------
## create class list ability  products for filter  
def get_abilitys(request,*args, **kwargs):
    ability_group = get_object_or_404(ExpertiseGroup,slug=kwargs['slug'])
    ability_list_id = ability_group.expertises_of_group.filter(is_active = True).values('ability_id')
    abilitys = Ability.objects.filter(pk__in=ability_list_id)\
                            .annotate(count = Count('ability'))\
                            .filter(~Q(count=0))\
                            .order_by('-count')
    return render(request,'specialtie_app/partials/ability_filter.html',{'abilitys':abilitys})
#--------------------------------------------------------------------
## create class list fieldwork_filter  products for filter  
def get_fieldworks(request,*args, **kwargs):
    fieldwork_group = get_object_or_404(ExpertiseGroup,slug=kwargs['slug'])
    fieldwork_list_id = fieldwork_group.expertises_of_group.filter(is_active = True).values('fieldwork_id')
    fieldworks = FieldWork.objects.filter(pk__in=fieldwork_list_id)\
                            .annotate(count = Count('fieldwork'))\
                            .filter(~Q(count=0))\
                            .order_by('-count')
    return render(request,'specialtie_app/partials/fieldwork_filter.html',{'fieldworks':fieldworks})
#--------------------------------------------------------------------
## create class list fieldwork_filter  products for filter  
def get_services(request,*args, **kwargs):
    service_group = get_object_or_404(ExpertiseGroup,slug=kwargs['slug'])
    service_list_id = service_group.expertises_of_group.filter(is_active = True).values('service_id')
    services = Services.objects.filter(pk__in=service_list_id)\
                            .annotate(count = Count('service'))\
                            .filter(~Q(count=0))\
                            .order_by('-count')
    return render(request,'specialtie_app/partials/service_filter.html',{'services':services})
#--------------------------------------------------------------------
## جزئیات محصول 
class ExpertDetaileView(View):
    def get(self,request,slug):
        expert = get_object_or_404(Expert,slug=slug)             
  
        if expert.is_active:
            return render (request,"specialtie_app/expert_details.html", {'expert':expert} )

#--------------------------------------------------------------------
## create related expert 
def get_related_experts(request,*args, **kwargs):
    current_prodouct = get_object_or_404(Expert,slug=kwargs['slug'])
    related_expert = []
    for group in current_prodouct.expertise_group.all():
        related_expert.extend(Expert.objects.filter(Q(is_active=True) & Q(expertise_group=group)& ~Q(id=current_prodouct.id)))
    return render (request,"specialtie_app/partials/related_experts.html" ,{'related_product':related_expert})
            

#--------------------------------------------------------------------
## Popular expert Group
def get_popular_expert_groups(request,*args, **kwargs):
    expert_groups = ExpertiseGroup.objects.filter(Q(is_active = True))\
                     .annotate(count = Count('expertises_of_group'))\
                     .order_by('-count')[:9]
    context = {
        "expert_groups" :expert_groups
    }
    return render (request,"specialtie_app/partials/popular_expert_groups.html",context)

#--------------------------------------------------------------------
## create class list page  is all  products 
class ExpertGroupView(View):
    def get(self, request):
        expert_groups = ExpertiseGroup.objects.filter(Q(is_active = True))\
                     .annotate(count = Count('expertises_of_group'))\
                     .order_by('-count')
        return render(request,"specialtie_app/expert_groups.html",{'expert_groups':expert_groups})
#------------------------------ filters --------------------------------------
## create class list group products for filter#دسته بندی کالاها برای فیلتر
def get_expert_groups(request):
    expert_groups =ExpertiseGroup.objects.annotate(count=Count('expertises_of_group'))\
                                        .filter(Q(is_active = True) & ~Q(count = 0))\
                                        .order_by('-count')  
    return render(request,'specialtie_app/partials/expert_groups.html',{'expert_groups':expert_groups})

   
#--------------------------------------------------------------------
## create class lists orther filters bar hasb feature products in the group
def get_feature_for_filter(request,*args, **kwargs):
    prodouct_group = get_object_or_404(ExpertiseGroup,slug=kwargs['slug'])
    feature_list =prodouct_group.Features_of_groups.all()
    feature_dict = dict()
    for feature in feature_list:
        feature_dict[feature] = feature.feature_value.all()
    return render(request,'product_app/partials/features_filter.html',{'feature_dict ':feature_dict })
    #--------------------------------------------------------------------
## create class lists orther filters bar hasb feature products in the group
def get_feature_for_filter(request,*args, **kwargs):
    prodouct_group = get_object_or_404(ExpertiseGroup,slug=kwargs['slug'])
    feature_list =prodouct_group.Features_of_groups.all()
    feature_dict = dict()
    for feature in feature_list:
        feature_dict[feature] = feature.featuer_value.all()
    return render(request,'specialtie_app/partials/features_filter.html',{'feature_dict ':feature_dict })
 
#-----------------------------------------------------------------------------------------------
## create def list page  is one of  products 
class ExpertsBygroupView(View):
    def get(self,request,*args, **kwargs):
        slug = kwargs['slug']
        current_group = get_object_or_404(ExpertiseGroup,slug=slug)
        experts = Expert.objects.filter(Q(is_active = True)& Q(expertise_group = current_group))  
        #--------------------------------------------
        ## Identity filter
        identity_filter = request.GET.getlist('identity')
        if identity_filter :
            experts = experts.filter(identity__id__in = identity_filter)
        #--------------------------------------------
        ## fieldwork filter
        fieldwork_filter = request.GET.getlist('fieldwork')
        if fieldwork_filter :
            experts = experts.filter(fieldwork__id__in = fieldwork_filter)
        #--------------------------------------------
        ## ability filter
        ability_filter = request.GET.getlist('ability')
        if ability_filter :
            experts = experts.filter(ability__id__in = ability_filter)
        #--------------------------------------------
        ## service filter
        service_filter = request.GET.getlist('service')
        if service_filter :
            experts = experts.filter(service__id__in = service_filter)
            
            
        group_slug = slug
        product_per_page = 10              
        paginator = Paginator(experts, product_per_page) 
        page_number = request.GET.get('page')       
        page_obj = paginator.get_page(page_number)   
        expert_count = experts.count(); 
        
        ##list numbers for make type open for number kala in page user
        show_count_product = []
        i = product_per_page
        while i < expert_count :
            show_count_product.append(i)
            i *= 2
        show_count_product.append(i)
            
        context = {
        'experts': experts,
        'current_group': current_group,
        'group_slug': group_slug,
        'page_obj': page_obj,
        'expert_count': expert_count,
        'show_count_product':show_count_product,
        'filter': filter,
        }
        return render(request,"specialtie_app/experts.html",context)
#----------------------------------------------------------------
## tow dropdown in admin panel
def get_filter_value_for_feature(request):  
    if request.method == 'GET':  
        feature_id = request.GET.get('feature_id')  
        feature_values = FeatureExpertValue.objects.filter(feature_id=feature_id)  
        res = {fv.value_title: fv.id for fv in feature_values}  
        return JsonResponse(res, safe=False)  
# ---------------------------------------------------------------------
## برای مجبور کردن مشتری برای ورودادامه پرداخت 
class CheckoutExpertView(LoginRequiredMixin, View):
    def get(self, request, expert_id):
        user = request.user
        customer = get_object_or_404(Customer, user=user)
        expert = get_object_or_404(Expert,id=expert_id)
        
      
            
        data = {
            'name' :user.name,
            'family':user.family,
            'email': user.email,
            'phone_number': customer.phone_number,
            # 'identity' :expert.identity,
            # 'ability' :expert.ability,
            'status' :expert.status,
            'address' :customer.address,
            'description' :expert.description,
            
        }
        form = ExpertForm(data)
         
        context = {
            'expert':expert,
            'form' : form, 
 
               
        }
        return render(request,'specialtie_app/partials/checkout_expert.html',context)
    #----------------------------------------------------------------
# for create AVg
def get_average_score_exp(request):  
    expertId = request.GET.get('expertId')  
    product = get_object_or_404(Expert, id=expertId)  
    scores = Expert.objects.filter(product=product)  

    if scores.exists():  
        average_score = scores.aggregate(Avg('score_exp'))['score_exp__avg']  
    else:  
        average_score = 0  

    return JsonResponse({'average_score': average_score})
#----------------------------------------------------------------
def add_score_exp(request):  
    expertId = request.GET.get('expertId')  
    score_exp = request.GET.get('score_exp')  

    expert = Expert.objects.get(id=expertId)  

    # ذخیره‌سازی امتیاز  
    ScoringExpert.objects.create(  
        expert=expert,  
        scoring_user=request.user,  
        score_exp=score_exp,  
    )   
    return JsonResponse({'message': 'امتیاز شما با موفقیت ثبت شد'})

from django.shortcuts import render,get_object_or_404,redirect
from .models import Product, Brand, ProductGroup,FeatureValue
from django.db.models import Q,Count,Min,Max
from django.views import View
from .filters import ProductFilter
from django.core.paginator import Paginator
from .compare import CompareProduct
from django.http import JsonResponse  
from django.http import HttpResponse
from django.db.models import Avg 

def get_root_group():
    return ProductGroup.objects.filter(Q(is_active = True)& Q(group_parent = None))

## ارزانترین محصولات
def get_cheapest_product(request,*args, **kwargs):
    products = Product.objects.filter(is_active = True).order_by('price')[:8]
    product_groups = get_root_group()
    context = {
        "products":products,
        "product_groups" :product_groups
    }
    return render (request,"product_app/partials/cheapest_product.html",context)
#--------------------------------------------------------------------
## جدیدترین محصولات(annotate)برای اضافه کردن فیلد یا ستون که برای شمارش وجمع و میانگین
def get_last_product(request,*args, **kwargs):
    products = Product.objects.filter(is_active = True).order_by('-published_date')[:6]
    product_groups = get_root_group()
    context = {
        "products":products,
        "product_groups" :product_groups
    }
    return render (request,"product_app/partials/last_product.html",context)
#--------------------------------------------------------------------
## گروه محصولات محبوب
def get_popular_product_groups(request,*args, **kwargs):
    product_groups = ProductGroup.objects.filter(Q(is_active = True))\
                     .annotate(count = Count('products_of_groups'))\
                     .order_by('-count')[:6]
    context = {
        "product_groups" :product_groups
    }
    return render (request,"product_app/partials/popular_product_groups.html",context)
#--------------------------------------------------------------------
## جزئیات محصول 
class productDetaileView(View):
    def get(self,request,slug):
        product = get_object_or_404(Product,slug = slug)
        if product.is_active:
            return render (request,"product_app/product_details.html",{'product':product})
#--------------------------------------------------------------------
## create related product 
def get_related_products(request,*args, **kwargs):
    current_prodouct = get_object_or_404(Product,slug=kwargs['slug'])
    related_product = []
    for group in current_prodouct.product_group.all():
        related_product.extend(Product.objects.filter(Q(is_active=True) & Q(product_group=group)& ~Q(id=current_prodouct.id)))
    return render (request,"product_app/partials/related_products.html" ,{'related_product':related_product})
            
#--------------------------------------------------------------------
## create class list page  is all  products 
class ProductGroupView(View):
    def get(self, request):
        product_groups = ProductGroup.objects.filter(Q(is_active = True))\
                     .annotate(count = Count('products_of_groups'))\
                     .order_by('-count')
        return render(request,"product_app/product_groups.html",{'product_groups':product_groups})
#------------------------------ filters --------------------------------------
## create class list group products for filter#دسته بندی کالاها برای فیلتر
def get_product_groups(request):
    product_groups =ProductGroup.objects.annotate(count=Count('products_of_groups'))\
                                        .filter(Q(is_active = True) & ~Q(count = 0))\
                                        .order_by('-count')
    
    return render(request,'product_app/partials/product_groups.html',{'product_groups':product_groups})

#--------------------------------------------------------------------
## create class list brands  products for filter فdلتر کالاهای براساس برند
def get_brands(request,*args, **kwargs):
    product_group = get_object_or_404(ProductGroup,slug=kwargs['slug'])
    brand_list_id = product_group.products_of_groups.filter(is_active = True).values('brand_id')
    brands = Brand.objects.filter(pk__in=brand_list_id)\
                            .annotate(count = Count('brands'))\
                            .filter(~Q(count=0))\
                            .order_by('-count')

    return render(request,'product_app/partials/brands_filter.html',{'brands':brands})
#--------------------------------------------------------------------
## create class lists orther filters bar hasb feature products in the group
def get_feature_for_filter(request,*args, **kwargs):
    product_group = get_object_or_404(ProductGroup,slug=kwargs['slug'])
    feature_list =product_group.features_of_groups.all()
    feature_dict = dict()
    for feature in feature_list:
        feature_dict[feature] = feature.feature_value.all()
 
    return render(request,'product_app/partials/features_filter.html',{'feature_dict ':feature_dict })


    #-----------------------------------------------------------------------------------------------
## create def list page  is one of  products 
class ProductsBygroupView(View):
    def get(self,request,*args, **kwargs):
        slug = kwargs['slug']
        current_group = get_object_or_404(ProductGroup,slug=slug)
        products = Product.objects.filter(Q(is_active = True) & Q(product_group = current_group))
        
        #--------------------------------------------
        ## price filter
        res_aggre = products.aggregate(min=Min('price'),max = Max('price'))
        filter = ProductFilter(request.GET,queryset = products)
        products = filter.qs
        
        #--------------------------------------------
        ## brand filter
        brands_filter = request.GET.getlist('brand')
        if brands_filter :
            products = products.filter(brand__id__in = brands_filter)
            
        #--------------------------------------------     
        ## features filter
        features_filter = request.GET.getlist('feature')
        if features_filter :
            products = products.filter(product_features__filter_value__id__in = features_filter).distinct()
             
        #--------------------------------------------  
        ## sort type
        sort_type = request.GET.get('sort_type')
        if not sort_type :
            sort_type = "0"
        elif sort_type == "1":
            products = products.order_by('price')
        elif sort_type == "2":
            products = products.order_by('-price')
            
        group_slug = slug
        product_per_page = 10                #تعداد کالاها در هر صفحه
        paginator = Paginator(products, product_per_page) 
        page_number = request.GET.get('page')       #بدست آوردن شماره صفحه جاری
        page_obj = paginator.get_page(page_number)  #صفحه بندی برای نمایش صفحه جاری
        product_count = products.count(); #تعداد کل مالاهای موجود در این گروه
        
        ##list numbers for make type open for number kala in page user
        show_count_product = []
        i = product_per_page
        while i < product_count :
            show_count_product.append(i)
            i *= 2
        show_count_product.append(i)
        context = {
           'products': products,
            'current_group': current_group,
            'res_aggre': res_aggre,
            'group_slug': group_slug,
            'page_obj': page_obj,
            'product_count': product_count,
            'show_count_product':show_count_product,
            'filter': filter,
            'sort_type': sort_type,
        }

        return render(request,"product_app/products.html",context)

#----------------------------------------------------------------
## tow dropdown in admin panel
def get_filter_value_for_feature(request):
    if request.method == 'GET':
        feature_id = request.GET['feature_id']
        feature_values = FeatureValue.objects.filter(feature_id=feature_id)
        res = {fv.value_title:fv.id for fv in feature_values}
        return JsonResponse(data=res, safe=False) 
#----------------------------------------------------------------
# ================================================================
# ۱. نمایش لیست مقایسه (نسخه کامل با مدیریت خطا)
# ================================================================
class ShowCompareListView(View):
    def get(self, request, *args, **kwargs):
        # ====== دریافت لیست مقایسه ======
        compare_list = CompareProduct(request)
        
        # ====== دریافت محصولات ======
        products = []
        if compare_list.compare_product:
            products = Product.objects.filter(id__in=compare_list.compare_product)
        
        # ====== دریافت ویژگی‌های محصولات ======
        features = []
        for product in products:
            # بررسی وجود product_features
            if hasattr(product, 'product_features'):
                for item in product.product_features.all():
                    if item.feature not in features:
                        features.append(item.feature)
        
        # ====== ساخت context ======
        context = {
            'compare_list': compare_list,
            'products': products,
            'features': features,
            'has_products': products.exists() if hasattr(products, 'exists') else False,
        }
        
        return render(request, 'product_app/compare_list.html', context)


# ================================================================
# ۲. دریافت امتیاز میانگین یک محصول (اصلاح‌شده)
# ================================================================
def get_average_score(request):
    # ====== دریافت productId ======
    productId = request.GET.get('productId')
    
    if not productId:
        return JsonResponse({
            'error': 'شناسه محصول ارسال نشده است',
            'average_score': 0
        }, status=400)
    
    # ====== دریافت محصول ======
    product = get_object_or_404(Product, id=productId)
    
    # ====== محاسبه میانگین امتیازات ======
    # توجه: باید مدل Score یا Comment داشته باشید
    # اگر مدل Comment دارید:
    # from apps.comments.models import Comment
    # scores = Comment.objects.filter(product=product)
    
    # اگر فیلد score در خود Product است:
    # average_score = Product.objects.filter(id=productId).aggregate(Avg('score'))['score__avg']
    
    # مثال با مدل فرضی Comment:
    try:
        from apps.comments.models import Comment
        scores = Comment.objects.filter(product=product)
        
        if scores.exists():
            average_score = scores.aggregate(Avg('score'))['score__avg']
            average_score = round(average_score, 2)  # گرد کردن به ۲ رقم اعشار
        else:
            average_score = 0
    except:
        # اگر مدل Comment وجود ندارد
        average_score = 0
    
    # ====== پاسخ JSON ======
    return JsonResponse({
        'success': True,
        'average_score': average_score,
        'product_id': productId,
        'product_name': product.product_name,
    })


# ================================================================
# ۳. (اختیاری) دریافت امتیاز برای چند محصول
# ================================================================
def get_products_score(request):
    productIds = request.GET.getlist('productIds[]')
    
    if not productIds:
        return JsonResponse({'error': 'شناسه محصول ارسال نشده است'}, status=400)
    
    result = {}
    for productId in productIds:
        try:
            product = Product.objects.get(id=productId)
            
            # محاسبه میانگین
            try:
                from apps.comments.models import Comment
                scores = Comment.objects.filter(product=product)
                avg = scores.aggregate(Avg('score'))['score__avg'] or 0
                result[productId] = round(avg, 2)
            except:
                result[productId] = 0
                
        except Product.DoesNotExist:
            result[productId] = None
    
    return JsonResponse({
        'success': True,
        'scores': result
    })


# ================================================================
# ۱. نمایش جدول کالاهای لیست مقایسه (اصلاح‌شده)
# ================================================================
def compare_table(request):
    # ====== دریافت لیست مقایسه ======
    compareList = CompareProduct(request)
    
    # ====== دریافت محصولات ======
    products = []
    for productId in compareList.compare_product:
        try:
            product = Product.objects.get(id=productId)
            products.append(product)
        except Product.DoesNotExist:
            # اگر محصول وجود نداشت، آن را از لیست حذف کن
            compareList.delete_form_compare_product(productId)
    
    # ====== دریافت ویژگی‌های محصولات ======
    features = []
    for product in products:
        for item in product.product_features.all():
            if item.feature not in features:
                features.append(item.feature)
    
    # ====== ساخت context ======
    context = {
        'products': products,
        'features': features,
    }
    
    # ====== رندر کردن صفحه ======
    return render(request, 'product_app/partials/compare_table.html', context)


# ================================================================
# ۲. محاسبه تعداد کالاهای موجود در لیست مقایسه
# ================================================================
def status_of_compare_list(request):
    compareList = CompareProduct(request)
    return HttpResponse(compareList.count)


# ================================================================
# ۳. اضافه کردن کالا به لیست مقایسه
# ================================================================
def add_to_compare_list(request):
    # ====== دریافت productId از درخواست ======
    productId = request.GET.get('productId')
    
    if not productId:
        messages.error(request, 'شناسه محصول ارسال نشده است')
        return redirect('products:compare_table')
    
    # ====== اضافه به لیست مقایسه ======
    compareList = CompareProduct(request)
    result = compareList.add_to_compare_product(productId)
    
    if result:
        messages.success(request, 'کالا به لیست مقایسه اضافه شد')
    else:
        messages.warning(request, 'امکان اضافه کردن کالا به لیست مقایسه وجود ندارد (حداکثر ۴ کالا)')
    
    # ====== بازگشت به صفحه قبلی ======
    next_url = request.META.get('HTTP_REFERER', 'products:compare_table')
    return redirect(next_url)


# ================================================================
# ۴. حذف کالا از لیست مقایسه
# ================================================================
def delete_from_compare_list(request):
    # ====== دریافت productId ======
    productId = request.GET.get('productId')
    
    if not productId:
        messages.error(request, 'شناسه محصول ارسال نشده است')
        return redirect('products:compare_table')
    
    # ====== حذف از لیست مقایسه ======
    compareList = CompareProduct(request)
    compareList.delete_form_compare_product(productId)
    
    messages.success(request, 'کالا از لیست مقایسه حذف شد')
    
    # ====== بازگشت به صفحه مقایسه ======
    return redirect('products:compare_table')


# ================================================================
# ۵. (اختیاری) حذف از طریق AJAX
# ================================================================
def delete_from_compare_ajax(request):
    productId = request.GET.get('productId')
    
    if productId:
        compareList = CompareProduct(request)
        compareList.delete_form_compare_product(productId)
        return HttpResponse('success')
    
    return HttpResponse('error', status=400)


# ================================================================
# ۶. (اختیاری) پاک کردن کل لیست مقایسه
# ================================================================
def clear_compare_list(request):
    compareList = CompareProduct(request)
    compareList.clear()
    messages.success(request, 'لیست مقایسه خالی شد')
    return redirect('products:compare_table')

from django.shortcuts import render, get_object_or_404, redirect 
from django.views import View
from .forms import CommentForm,CommentExpertForm
from apps.comment_scoring_favorites.models import Comment,CommentExpert
from apps.products.models import Product
from apps.specialties.models import Expert
from django.contrib import messages
from django.http import HttpResponse
from apps.comment_scoring_favorites.models import Scoring, Favorite,ScoringExpert
from django.db.models import Q
from apps.orders.shop_cart import ShopCart
from django.http import JsonResponse 
 
#----------------------------------------------------------------
## create a commentView with a form
class CommantView(View):
    def get(self,request, *args, **kwargs):
        productId = request.GET.get('productId')
        commentId = request.GET.get('commentId')
        slug = kwargs['slug']
        initial_dict = {
            "product_id": productId,
            "comment_id": commentId,
        }
        form = CommentForm(initial = initial_dict)
        return render(request, 'csf_app/partials/create_comment.html', {'form' :form, 'slug': slug})
   
    def post (self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            parent = None
            if (cd['comment_id']):
                parentId = cd['comment_id'] 
                parent = Comment.objects.get(id=parentId)   
            Comment.objects.create(
                                product = product,
                                commenting_user = request.user,
                                comment_text = cd['comment_text'],
                                comment_parent = parent,
                                
                                )  
            messages.success(request, 'نظر شما با موفقیت ثبت شد')
            return redirect('products:product_details',product.slug)
        messages.error(request, 'خطا در ارسال نظر','danger')
        return redirect('products:product_details',product.slug)
#----------------------------------------------------------------
 
## create a commentexpertView with a form
class CommantExpertView(View):
    def get(self,request, *args, **kwargs):
        expertId = request.GET.get('expertId')
        commentId = request.GET.get('commentId')
        slug = kwargs['slug']
        initial_dict = {
            "expert_Id": expertId,
            "comment_id": commentId,
        }
        form = CommentExpertForm(initial = initial_dict)
        return render(request, 'csf_app/partials/create_comment_expert.html', {'form' :form, 'slug': slug})
   
    def post (self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        expert = get_object_or_404(Expert, slug=slug)
        form = CommentExpertForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            parent = None
            if (cd['expert_id']):
                parentId = cd['expert_id'] 
                parent = CommentExpert.objects.get(id=parentId)   
            CommentExpert.objects.create(
                                expert = expert,
                                commenting_user = request.user,
                                comment_text = cd['comment_text'],
                                comment_parent = parent,
                                
                                )  
            messages.success(request, 'نظر شما با موفقیت ثبت شد')
            return redirect('specialties:expert_details',expert.slug)
        messages.error(request, 'خطا در ارسال نظر','danger')
        return redirect('specialties:expert_details',expert.slug)
#--------------------------------------
# create add score function
def add_score(request):
    productId = request.GET.get('productId')
    score = request.GET.get('score')
    
    product = Product.objects.get(id=productId)
    
    Scoring.objects.create(
        product=product,
        scoring_user = request.user,
        score = score,
    ) 
    return HttpResponse ('امتیاز شما با موفقیت ثبت شد')
# # ===============================
# def add_scoreexpert(request):
#     expertId = request.GET.get('expertId')
#     score = request.GET.get('score')
    
#     expert = Product.objects.get(id=expertId)
    
#     Scoring.objects.create(
#         expert=expert,
#         scoring_user = request.user,
#         score = score,
#     ) 
#     return HttpResponse ('امتیاز شما با موفقیت ثبت شد')
# # ===============================
def add_scoreexpert(request):  
    expertId = request.GET.get('expertId')  
    score_exp = request.GET.get('score_exp')  

    expert = Expert.objects.get(id=expertId)  

    # ذخیره‌سازی امتیاز  
    ScoringExpert.objects.create(  
        expert=expert,  
        scoring_user=request.user,  
        score_exp=score_exp,  
    )   
    return HttpResponse('امتیاز شما با موفقیت ثبت شد')
#----------------------------------------------------------------
##create a add favorite
def add_to_favorite(request):
    productId = request.GET.get('productId')
    product = Product.objects.get(id=productId)
    flag = Favorite.objects.filter(
                                    Q(favorite_user_id=request.user.id) & 
                                    Q(product_id=productId)).exists()
    if (not flag):
        Favorite.objects.create(
            product=product,
            favorite_user = request.user,
            )
        return HttpResponse('این کالا به لیست علایق شما اضافه شد')
    return  HttpResponse('این کالا قبلا در لیست علایق شما قرار گرفته')
          
#----------------------------------------------------------------
class  UserFavoriteView(View):
    def get(self, request, *args, **kwargs):
        user_favorite_product = Favorite.objects.filter(Q(favorite_user_id=request.user.id))
        return render(request, 'csf_app/user_favorite.html', {'user_favorite_product': user_favorite_product}) 
# ---------------------------------------------------------------------
# تابع برای اضافه کردن به سبد علایق
# def add_to_product_fvorite(request):
#     product_id = request.GET.get('product_id')
#     qty = request.GET.get('qty')
#     shop_cart = ShopCart(request)
#     product = get_object_or_404(Product,id = product_id)
#     shop_cart.add_to_shop_cart(product, qty)
#     return  HttpResponse(shop_cart.count)                          
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
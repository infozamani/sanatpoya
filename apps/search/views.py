from django.shortcuts import render
from django.views import View
from apps.products.models import Product
from apps.blog.models import Blog
from apps.specialties.models import ExpertiseGroup
from django.db.models import Q
#----------------------------------------------------------------
## Creating search results class
class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        products = Product.objects.filter(
            Q(product_name__icontains=query) | 
            Q(description__icontains=query)  
        )
        blogs = Blog.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) 
        )
        specialties = ExpertiseGroup.objects.filter(
            Q(group_title__icontains=query) | 
            Q(description__icontains=query) 
        ) 
        context = {
            'products' : products,
            'blogs' : blogs,
            'specialties' : specialties,
        }
        return render(request,'search_apps/search_results.html',context)
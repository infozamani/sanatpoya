from django.shortcuts import render,redirect
from django.conf import settings
from django.views import View
from .models import Slider,AboutUs,Post
from .forms import PostForm
from apps.specialties.models import Expert
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView 
from django.views.generic.edit import CreateView,FormMixin,UpdateView,DeleteView
from django.contrib import messages

#----------------------------------------------------------------
from django.utils import timezone
from apps.advertisement.models import Advertisement   


from django.shortcuts import render
from django.conf import settings
from apps.advertisement.models import Advertisement
from django.utils import timezone
from apps.blog.models import Blog 

def index(request):
    """صفحه اصلی با نمایش تبلیغات"""
    ads = Advertisement.objects.filter(
        is_active=True,
        expiry_date__gt=timezone.now()
    ).order_by('order', '-created_at')
    latest_blogs = Blog.objects.filter(is_active=True).order_by('-id')[:6]
    
    # for ad in ads:
    #     print(f"عنوان: {ad.title}, تصویر: {ad.image_name.url if ad.image_name else 'ندارد'}")
    
    context = {
        'ads': ads,
        'latest_blogs': latest_blogs,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'main_app/index.html', context)
 
def home(request):
    """صفحه اصلی (تکرار)"""
    return index(request)
#----------------------------------------------------------------
def shop (request):
    return render(request,'main_app/shop.html')
#----------------------------------------------------------------
def realestate (request):
    return render(request,'main_app/shop_realestate.html')
#----------------------------------------------------------------
##about-us
class AboutUsView(View):
    def get(self, request):
        abouts = AboutUs.objects.all()
        
      
        return render(request,'main_app/about-us.html',{'abouts':abouts, })
#----------------------------------------------------------------
##context_us
def create_post(request):  
    if request.method == 'POST':  
        form = PostForm(request.POST)  
        if form.is_valid():  
            form.save()  # همچنین می‌توانید مستقیماً استفاده کنید.  
            messages.success(request,"پست با موفقیت ارسال شد")
            return redirect("main:index")  # یا هر URL دیگری که مدنظرتان است 
    else:   
        form = PostForm()  # برای نمایش فرم خالی  

    context = {  
        "form": form,
    }  
  
    return render(request, 'main_app/context_us.html', context)  
       
#----------------------------------------------------------------
def regulations (request):
     return render(request, 'main_app/regulations.html')  
# ----------------------------------------------------------------
class SliderView(View):
     def get(self, request):
         sliders = Slider.objects.filter(is_active=True)
         return render(request,'main_app/sliders.html',{'sliders':sliders})
     
 
from django.conf import settings

def media_admin(request):
    """
    Context processor برای ارسال MEDIA_URL به تمام قالب‌ها
    """
    return {
        'media_url': settings.MEDIA_URL,
    }


from django.shortcuts import render
from .models import Advertisement
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import AdvertisementForm  

def advertisement_list(request):
    ads = Advertisement.objects.all()
    # ارسال media_url به template
    context = {
        'ads': ads,
        'media_url': settings.MEDIA_URL,
    }
    return render(request, 'advertisement/advertisement_list.html', context)


def advertisement_list(request):
    ads = Advertisement.objects.all()
    return render(request, 'advertisement/advertisement_list.html', {'ads': ads})

# این تابع را از حالت کامنت خارج کنید
def advertisement_create(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('advertisements:advertisement_list')  # به لیست تبلیغات هدایت می‌کند
    else:
        form = AdvertisementForm()
    
    return render(request, 'advertisement/advertisement_form.html', {'form': form})
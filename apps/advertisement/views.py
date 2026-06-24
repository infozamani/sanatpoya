from django.shortcuts import render  
from .models import Advertisement  

def advertisement_list(request):  
    ads = Advertisement.objects.all()  
    return render(request, 'advertisement/advertisement_list.html', {'ads': ads})

# def advertisement_create(request):  
#     if request.method == 'POST':  
#         form = AdvertisementForm(request.POST, request.FILES)  
#         if form.is_valid():  
#             form.save()  
#             return redirect('advertisement_list')  # به لیست تبلیغات هدایت می‌کند  
#     else:  
#         form = AdvertisementForm()  
    
#     return render(request, 'advertisement_form.html', {'form': form})
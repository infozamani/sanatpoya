# views.py  
from django.shortcuts import render, redirect  
from django.core.mail import send_mail  
from django.conf import settings  
from .forms import ContactForm  
from .models import ContactMessage  # اگر مدل را ایجاد کرده‌اید  

def contact_view(request):  
    if request.method == 'POST':  
        form = ContactForm(request.POST)  
        if form.is_valid():  
            name = form.cleaned_data['name']  
            email = form.cleaned_data['email']  
            message = form.cleaned_data['message']  
            
            # save email to database
            ContactMessage.objects.create(name=name, email=email, message=message)  

            # send email
            send_mail(  
                f'پیام جدید از {name}',  # title email 
                message,    
                email,   
                [settings.DEFAULT_FROM_EMAIL],   
                fail_silently=False,  
            )  

            return redirect('contact_success')  # صفحه موفقیت بعد از ارسال پیام  

    else:  
        form = ContactForm()  
    
    return render(request, 'emailer_app/contact.html', {'form': form})
from django import forms  
from .models import Ticket, TicketReply  

class TicketForm(forms.ModelForm):  
    class Meta:  
        model = Ticket  
        fields = ['title', 'description']    
        widgets = {  
            'title': forms.TextInput(attrs={  
                'class': 'form-control',    
                'placeholder': 'عنوان تیکت را وارد کنید',  
            }),  
            'description': forms.Textarea(attrs={  
                'class': 'form-control',  
                'placeholder': 'توضیحات تیکت را وارد کنید',  
                'rows': 5,    
            }),  
        }  
    
    def __init__(self, *args, **kwargs):  
        super(TicketForm, self).__init__(*args, **kwargs)  
        self.fields['title'].label = "عنوان تیکت"  
        self.fields['description'].label = "توضیحات تیکت"  


class TicketReplyForm(forms.ModelForm):  
    class Meta:  
        model = TicketReply  
        fields = ['message']  # فقط فیلد پیام را می‌خواهیم  
        widgets = {  
            'message': forms.Textarea(attrs={  
                'class': 'form-control',  
                'placeholder': 'پاسخ خود را وارد کنید',  
                'rows': 5,  # تعداد ردیف‌های نمایش داده شده  
            }),  
        }  

    def __init__(self, *args, **kwargs):  
        super(TicketReplyForm, self).__init__(*args, **kwargs)  
        self.fields['message'].label = "پاسخ"

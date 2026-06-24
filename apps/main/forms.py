from django import forms
from .models import Post 
 
#  Chice_Payment_type = ((1,'درگاه بانکی '), (2,'پرداخت در محل'),(3,'فیش بانکی '))
# class PostForm(forms.Form):
#     name = forms.CharField(label="", 
#                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' :'نام'}),
#                         error_messages={'required': ' این فیلد نباید خالی بماند'})
#     title = forms.CharField(label="", 
#                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' :'عنوان پست '}),
#                         error_messages={'required': 'این فیلد نباید خالی بماند'})
#     description = forms.CharField(label="", 
#                         widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder' :'توضیحات ','rows':'4'}),
#                         required=False)
#     email = forms.CharField(label="", 
#                         widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder' :'ایمیل'}),
#                         required=False)
class PostForm(forms.ModelForm):  
    class Meta:  
        model = Post  # مدل مرتبط  
        fields = ['name', 'title', 'email' ,'descriptions',]
    
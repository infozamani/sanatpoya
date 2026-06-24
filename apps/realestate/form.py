from django import forms

class ExpertForm(forms.Form):
    name = forms.CharField(label="", 
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' :'نام'}),
                        error_messages={'required': ' این فیلد نباید خالی بماند'})
    family = forms.CharField(label="", 
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' :'خانوادگی '}),
                        error_messages={'required': 'این فیلد نباید خالی بماند'})
    email = forms.EmailField(label="", 
                        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder' :'ایمیل'}),
                        required=False)
    
    phone_number = forms.CharField(label="", 
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' :'تلفن'}),
                        required=False)
    # identity = forms.CharField(label="", 
    #                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' :'حقیقی'}),
    #                     error_messages={'required': 'این فیلد نباید خالی بماند'})
    ability = forms.CharField(label="", 
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' :'توانمدی'}),
                        error_messages={'required': 'این فیلد نباید خالی بماند'})
    status = forms.CharField(label="", 
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' :'مدرک تحصیلی'}),
                        error_messages={'required': 'این فیلد نباید خالی بماند'})
    
    address = forms.CharField(label="", 
                        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder' :'آدرس', 'rows':'3'}),
                        error_messages={'required': 'این فیلد نباید خالی بماند'})
    
    description = forms.CharField(label="", 
                        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder' :'توضیحات ','rows':'4'}),
                        required=False)
  
    
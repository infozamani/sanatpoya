from django.forms import ModelForm
from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# ================================================================
# 1. فرم ایجاد کاربر (برای ادمین)
# ================================================================
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور را وارد کنید'
        })
    )
    password2 = forms.CharField(
        label="Repassword",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'تکرار رمز عبور را وارد کنید'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['mobile_number', 'email', 'name', 'family', 'gender']
        widgets = {
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره موبایل را وارد کنید',
                'dir': 'ltr'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل را وارد کنید'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام را وارد کنید'
            }),
            'family': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی را وارد کنید'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }, choices=CustomUser.GENDER_CHOICES),
        }
    
    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور وارد شده با هم مغایرت دارد')
        if pass2 and len(pass2) < 8:
            raise ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد')
        return pass2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# ================================================================
# 2. فرم تغییر کاربر (برای ادمین)
# ================================================================
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='برای تغییر رمز عبور روی <a href="../password/">کلیک</a> کنید.'
    )
    
    class Meta:
        model = CustomUser
        fields = ['mobile_number', 'password', 'email', 'name', 'family', 'gender', 'is_active', 'is_admin']
        widgets = {
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'dir': 'ltr'
            }),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'family': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}, choices=CustomUser.GENDER_CHOICES),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_admin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ================================================================
# 3. فرم ثبت‌نام کاربر (کامل با همه فیلدها)
# ================================================================
class RegisterUserForm(ModelForm):
    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور خود را وارد کنید',
            'id': 'id_password1'
        }),
        error_messages={'required': 'رمز عبور نمی‌تواند خالی باشد'}
    )
    
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'تکرار رمز عبور را وارد کنید',
            'id': 'id_password2'
        }),
        error_messages={'required': 'تکرار رمز عبور نمی‌تواند خالی باشد'}
    )
    
    class Meta:
        model = CustomUser
        fields = ['mobile_number', 'name', 'family', 'email', 'gender']
        widgets = {
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره موبایل را وارد کنید',
                'id': 'id_mobile_number',
                'dir': 'ltr'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خود را وارد کنید',
                'id': 'id_name'
            }),
            'family': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی خود را وارد کنید',
                'id': 'id_family'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل خود را وارد کنید (اختیاری)',
                'id': 'id_email'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_gender'
            }, choices=CustomUser.GENDER_CHOICES),
        }
        labels = {
            'mobile_number': 'شماره موبایل',
            'name': 'نام',
            'family': 'نام خانوادگی',
            'email': 'ایمیل',
            'gender': 'جنسیت',
        }
        help_texts = {
            'mobile_number': 'شماره موبایل باید ۱۱ رقم باشد و با ۰۹ شروع شود',
            'email': 'ایمیل اختیاری است',
        }
    
    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number')
        if mobile:
            mobile = mobile.replace(' ', '').replace('-', '')
            if not mobile.isdigit():
                raise ValidationError('شماره موبایل باید فقط شامل اعداد باشد')
            if len(mobile) != 11:
                raise ValidationError('شماره موبایل باید ۱۱ رقم باشد')
            if not mobile.startswith('09'):
                raise ValidationError('شماره موبایل باید با ۰۹ شروع شود')
            if CustomUser.objects.filter(mobile_number=mobile).exists():
                raise ValidationError('این شماره موبایل قبلاً ثبت شده است')
        return mobile
    
    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور و تکرار آن مطابقت ندارند')
        if pass2 and len(pass2) < 8:
            raise ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد')
        return pass2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# ================================================================
# 4. فرم تأیید کد فعال‌سازی
# ================================================================
class VerifyRegisterForm(forms.Form):
    active_code = forms.CharField(
        label='کد فعال‌سازی',
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'کد 5 رقمی دریافتی را وارد کنید',
            'id': 'id_active_code',
            'maxlength': '5',
            'dir': 'ltr'
        })
    )
    
    def clean_active_code(self):
        code = self.cleaned_data.get('active_code')
        if code:
            if not code.isdigit():
                raise ValidationError('کد فعال‌سازی باید فقط شامل اعداد باشد')
            if len(code) != 5:
                raise ValidationError('کد فعال‌سازی باید ۶ رقم باشد')
        return code


# ================================================================
# 5. فرم ورود
# ================================================================
class LoginUserForm(forms.Form):
    mobile_number = forms.CharField(
        label='شماره موبایل',
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'شماره موبایل را وارد کنید',
            'id': 'id_mobile_number',
            'dir': 'ltr'
        })
    )
    
    password = forms.CharField(
        label='رمز عبور',
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور خود را وارد کنید',
            'id': 'id_password'
        })
    )
    
    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number')
        if mobile:
            mobile = mobile.replace(' ', '').replace('-', '')
            if not mobile.isdigit():
                raise ValidationError('شماره موبایل باید فقط شامل اعداد باشد')
            if len(mobile) != 11:
                raise ValidationError('شماره موبایل باید ۱۱ رقم باشد')
        return mobile


# ================================================================
# 6. فرم تغییر رمز عبور
# ================================================================
# ================================================================
# 6. فرم تغییر رمز عبور (بدون رمز فعلی)
# ================================================================
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(
        label='رمز عبور جدید',
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید را وارد کنید',
            'id': 'id_password1'
        })
    )
    
    password2 = forms.CharField(
        label='تکرار رمز عبور جدید',
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'تکرار رمز عبور جدید را وارد کنید',
            'id': 'id_password2'
        })
    )
    
    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور و تکرار آن مطابقت ندارند')
        
        if pass2 and len(pass2) < 8:
            raise ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد')
        
        return pass2

# ================================================================
# 7. فرم فراموشی رمز عبور (نام اصلاح‌شده)
# ================================================================
class RememberPasswordForm(forms.Form):  # ✅ نام صحیح
    mobile_number = forms.CharField(
        label='شماره موبایل',
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'شماره موبایل را وارد کنید',
            'id': 'id_mobile_number',
            'dir': 'ltr'
        })
    )
    
    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number')
        if mobile:
            mobile = mobile.replace(' ', '').replace('-', '')
            if not mobile.isdigit():
                raise ValidationError('شماره موبایل باید فقط شامل اعداد باشد')
            if len(mobile) != 11:
                raise ValidationError('شماره موبایل باید ۱۱ رقم باشد')
            if not CustomUser.objects.filter(mobile_number=mobile).exists():
                raise ValidationError('این شماره موبایل در سیستم ثبت نشده است')
        return mobile


# ================================================================
# 8. فرم ویرایش پروفایل (کامل با تصویر)
# ================================================================
class UpdateProfileForm(forms.Form):
    mobile_number = forms.CharField(
        label="شماره موبایل",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'شماره موبایل',
            'readonly': 'readonly',
            'id': 'id_mobile_number',
            'dir': 'ltr'
        })
    )
    
    name = forms.CharField(
        label="نام",
        error_messages={'required': 'این فیلد نمی‌تواند خالی باشد'},
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام خود را وارد کنید',
            'id': 'id_name'
        })
    )
    
    family = forms.CharField(
        label="نام خانوادگی",
        error_messages={'required': 'این فیلد نمی‌تواند خالی باشد'},
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام خانوادگی خود را وارد کنید',
            'id': 'id_family'
        })
    )
    
    email = forms.EmailField(
        label="ایمیل",
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل خود را وارد کنید',
            'id': 'id_email'
        })
    )
    
    phone_number = forms.CharField(
        label="تلفن ثابت",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'تلفن ثابت خود را وارد کنید',
            'id': 'id_phone_number',
            'dir': 'ltr'
        })
    )
    
    address = forms.CharField(
        label="آدرس",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'آدرس خود را وارد کنید',
            'id': 'id_address',
            'rows': 3
        })
    )
    
    image = forms.ImageField(
        label="تصویر پروفایل",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control-file',
            'id': 'id_image',
            'accept': 'image/*'
        })
    )
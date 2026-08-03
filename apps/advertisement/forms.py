from django import forms
from django.core.exceptions import ValidationError
from .models import Advertisement
import re
from django_ckeditor_5.widgets import CKEditor5Widget

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'image_name', 'url']
        widgets = {
            'description': CKEditor5Widget(config_name='default'),
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'مثال: تخفیف ویژه محصولات صنعت پویا',
                'maxlength': '100',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'توضیحات کامل تبلیغ خود را اینجا بنویسید...',
                'rows': 6,
                'cols': 50,
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://example.com/product',
            }),
        }
        labels = {
            'title': 'عنوان تبلیغ',
            'description': 'توضیحات',
            'image_name': 'تصویر تبلیغ',
            'url': 'لینک',
        }
        help_texts = {
            'title': 'حداکثر ۱۰۰ کاراکتر',
            'description': 'توضیحات کامل و جذاب برای جذب مخاطب',
            'image_name': 'فرمت‌های مجاز: JPG, PNG, GIF, WebP (حداکثر ۵ مگابایت)',
            'url': 'لینک معتبر و فعال (با https:// شروع شود)',
        }
        error_messages = {
            'title': {
                'required': 'وارد کردن عنوان تبلیغ الزامی است',
                'max_length': 'عنوان نمی‌تواند بیشتر از ۱۰۰ کاراکتر باشد',
            },
            'url': {
                'required': 'وارد کردن لینک الزامی است',
                'invalid': 'لطفاً یک لینک معتبر وارد کنید',
            },
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            # حذف فاصله‌های اضافی
            title = ' '.join(title.split())
            # بررسی طول بعد از تمیز کردن
            if len(title) < 5:
                raise ValidationError('عنوان باید حداقل ۵ کاراکتر باشد')
            if len(title) > 100:
                raise ValidationError('عنوان نمی‌تواند بیشتر از ۱۰۰ کاراکتر باشد')
            # بررسی کلمات تکراری
            words = title.split()
            if len(words) > len(set(words)) * 2:  # اگر کلمات تکراری بیش از حد باشد
                raise ValidationError('عنوان دارای کلمات تکراری بیش از حد است')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            # حذف فاصله‌های اضافی
            description = ' '.join(description.split())
            if len(description) < 20:
                raise ValidationError('توضیحات باید حداقل ۲۰ کاراکتر باشد')
            if len(description) > 2000:
                raise ValidationError('توضیحات نمی‌تواند بیشتر از ۲۰۰۰ کاراکتر باشد')
            # بررسی لینک‌های مخرب
            suspicious_patterns = [
                r'<script', r'javascript:', r'onclick=', r'onload=',
                r'alert\(', r'console\.', r'eval\(', r'document\.'
            ]
            for pattern in suspicious_patterns:
                if re.search(pattern, description, re.IGNORECASE):
                    raise ValidationError('توضیحات حاوی کدهای مخرب است')
        return description

    def clean_image_name(self):
        image = self.cleaned_data.get('image_name')
        if image:
            # بررسی حجم فایل (حداکثر ۵ مگابایت)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('حجم تصویر نباید بیشتر از ۵ مگابایت باشد')
            
            # بررسی پسوند فایل
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']
            ext = image.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise ValidationError(f'فرمت فایل مجاز نیست. فرمت‌های مجاز: {", ".join(valid_extensions)}')
            
            # بررسی نسبت تصویر (اختیاری)
            from PIL import Image
            from io import BytesIO
            try:
                img = Image.open(BytesIO(image.read()))
                width, height = img.size
                # نسبت تصویر بین 1:3 تا 3:1 باشد
                ratio = width / height
                if ratio < 0.33 or ratio > 3:
                    raise ValidationError('نسبت تصویر باید بین ۱:۳ تا ۳:۱ باشد')
                # حداقل ابعاد
                if width < 300 or height < 200:
                    raise ValidationError('حداقل ابعاد تصویر باید ۳۰۰×۲۰۰ پیکسل باشد')
                # حداکثر ابعاد
                if width > 4000 or height > 4000:
                    raise ValidationError('حداکثر ابعاد تصویر ۴۰۰۰×۴۰۰۰ پیکسل است')
            except Exception:
                raise ValidationError('فایل انتخاب شده یک تصویر معتبر نیست')
            
            # ریست کردن pointer تصویر برای استفاده دوباره
            image.seek(0)
        return image

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url:
            # اطمینان از وجود پروتکل
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # بررسی دامنه‌های مجاز (اختیاری)
            # domain = url.split('/')[2]
            # allowed_domains = ['example.com', 'industrypooya.com', 'google.com']
            # if not any(domain.endswith(d) for d in allowed_domains):
            #     raise ValidationError('دامنه لینک مجاز نیست')
            
            # بررسی لینک‌های مخرب
            suspicious_patterns = [
                r'\.exe$', r'\.zip$', r'\.rar$', r'\.bat$',
                r'\.js$', r'\.php\?', r'cmd=', r'exec='
            ]
            for pattern in suspicious_patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    raise ValidationError('لینک حاوی پسوند یا پارامتر مخرب است')
            
            # بررسی طول
            if len(url) > 500:
                raise ValidationError('لینک نمی‌تواند بیشتر از ۵۰۰ کاراکتر باشد')
            
            # بررسی وجود کاراکترهای غیرمجاز
            if ' ' in url:
                raise ValidationError('لینک نباید شامل فاصله باشد')
            
            # بررسی فرمت لینک
            url_pattern = re.compile(
                r'^https?://'  # http:// یا https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # دامنه
                r'localhost|'  # localhost
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # یا IP
                r'(?::\d+)?'  # پورت (اختیاری)
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            
            if not url_pattern.match(url):
                raise ValidationError('فرمت لینک معتبر نیست')
                
        return url

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        
        # بررسی تکراری بودن عنوان (اختیاری)
        if title and Advertisement.objects.filter(title=title).exists():
            if not self.instance.pk or self.instance.title != title:
                raise ValidationError('یک تبلیغ با این عنوان قبلاً ثبت شده است')
        
        # بررسی وجود کلمات کلیدی در توضیحات
        if title and description:
            title_words = set(title.lower().split())
            desc_words = set(description.lower().split())
            common_words = title_words.intersection(desc_words)
            if len(common_words) < 2:
                raise ValidationError('توضیحات باید حداقل شامل ۲ کلمه از عنوان باشد')
        
        return cleaned_data
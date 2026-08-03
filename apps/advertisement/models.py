from django.db import models
from utils import FileUpload
from django.utils import timezone
from datetime import timedelta

class Advertisement(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان تبلیغ')
    description = models.TextField(verbose_name='توضیحات تبلیغ')
    file_upload = FileUpload('images', 'advertisement')
    image_name = models.ImageField(
        upload_to=file_upload.upload_to, 
        verbose_name='تصویر تبلیغات',
        help_text='تصویر با کیفیت و مرتبط با تبلیغ'
    )
    url = models.URLField(max_length=200, verbose_name='لینک')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    # فیلدهای جدید
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    views_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    order = models.IntegerField(default=0, verbose_name='ترتیب نمایش', help_text='عدد کمتر = نمایش بالاتر')
    
    expiry_date = models.DateTimeField(
        verbose_name='تاریخ انقضا',
        default=timezone.now() + timedelta(days=30),  
        help_text='تاریخ و زمانی که تبلیغ منقضی می‌شود'
    )
    class Meta:
        verbose_name = 'تبلیغ'
        verbose_name_plural = 'تبلیغات'
        ordering = ['-is_active', 'order', '-created_at']

    def __str__(self):
        return self.title
    
    def increase_view(self):
        """افزایش تعداد بازدید"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def is_expired(self):
        """بررسی منقضی شدن تبلیغ"""
        return timezone.now() > self.expiry_date
    
    def save(self, *args, **kwargs):
        """اگر تاریخ انقضا گذشته، غیرفعال کن"""
        if self.expiry_date and timezone.now() > self.expiry_date:
            self.is_active = False
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'تبلیغ'
        verbose_name_plural = 'تبلیغات'
        ordering = ['-is_active', 'order', '-created_at']

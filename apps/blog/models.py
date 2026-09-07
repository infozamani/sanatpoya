# apps/blog/models.py

from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse  # <--- این خط را اضافه کن


class Author(models.Model):
    name = models.CharField(max_length=30, verbose_name='نام')
    family = models.CharField(max_length=30, verbose_name='نام خانوادگی')
    slug = models.SlugField(max_length=30)
    age = models.IntegerField(default=30, verbose_name='سن')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    register_data = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ثبت')
    email = models.EmailField(max_length=100, verbose_name='ایمیل')
    image_name = models.CharField(default='nophpont.png', blank=True, null=True, max_length=200, verbose_name='تصویر')

    def __str__(self):
        return f"{self.name} {self.family}"


class Blog(models.Model):
    author = models.ForeignKey(Author, verbose_name="نویسنده", on_delete=models.CASCADE, related_name='authors')
    title = models.CharField(verbose_name='عنوان مقاله', max_length=50)
    summery_description = models.TextField(default="", blank=True, null=True, verbose_name='خلاصه مقاله')
    description = RichTextUploadingField(config_name='special', blank=True, null=True, verbose_name='توضیحات کامل مقاله')
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال', default=True)
    main_image = models.ImageField(upload_to='images/blogimg/', verbose_name='تصویر اصلی مقاله')
    register_data = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ثبت')

    # ====== فیلدهای جدید سئو (SEO) ======
    seo_title = models.CharField(
        max_length=70, 
        blank=True, 
        verbose_name='عنوان سئو (حداکثر 70 کاراکتر)',
        help_text='اگر خالی باشد، عنوان اصلی استفاده می‌شود'
    )
    meta_description = models.CharField(
        max_length=160, 
        blank=True, 
        verbose_name='توضیحات متا (حداکثر 160 کاراکتر)',
        help_text='خلاصه‌ای جذاب از مقاله برای نمایش در نتایج گوگل'
    )
    meta_keywords = models.CharField(
        max_length=255, 
        blank=True, 
        verbose_name='کلمات کلیدی',
        help_text='با کاما جدا کنید: آموزش، جنگو، سئو'
    )
    focus_keyword = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name='کلمه کلیدی اصلی',
        help_text='کلمه کلیدی که می‌خواهید مقاله برای آن رتبه بگیرد'
    )

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('blogs:post_blog', args=[str(self.id)])
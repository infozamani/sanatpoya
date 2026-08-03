#!/usr/bin/env python
# seed.py - بارگذاری داده‌های نمونه برای تبلیغات

import os
import sys
import django
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
from datetime import timedelta

# تنظیم محیط Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sanatpoya.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

# ✅ حالا می‌توانیم از timezone استفاده کنیم
from django.utils import timezone
from apps.advertisement.models import Advertisement


def create_dummy_image(text, width=800, height=600):
    """ایجاد تصویر ساختگی با متن"""
    colors = [
        (41, 128, 185),   # آبی
        (46, 204, 113),   # سبز
        (231, 76, 60),    # قرمز
        (155, 89, 182),   # بنفش
        (243, 156, 18),   # نارنجی
        (52, 152, 219),   # آبی روشن
        (39, 174, 96),    # سبز تیره
        (142, 68, 173),   # بنفش تیره
    ]
    
    img = Image.new('RGB', (width, height), color=random.choice(colors))
    draw = ImageDraw.Draw(img)
    
    # رسم مستطیل سفید برای متن
    draw.rectangle([(width//4, height//3), (width*3//4, height*2//3)], fill=(255, 255, 255, 200))
    draw.rectangle([(width//4, height//3), (width*3//4, height*2//3)], outline=(0, 0, 0, 50), width=2)
    
    # نوشتن متن
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/Arial.ttf", 36)
        except:
            font = ImageFont.load_default()
    
    # شکستن متن به چند خط
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if len(' '.join(current_line)) > 15:
            lines.append(' '.join(current_line[:-1]))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    
    # رسم متن در مرکز
    y_position = height//2 - (len(lines) * 20)
    for line in lines:
        draw.text((width//2, y_position), line, fill=(0, 0, 0), font=font, anchor="mm")
        y_position += 40
    
    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=90)
    img_io.seek(0)
    return ContentFile(img_io.getvalue(), name=f'seed_{random.randint(1000, 9999)}.jpg')


# ✅ داده‌های نمونه با تاریخ انقضا
ads_data = [
    {
        'title': 'مبل سلطنتی لوکس',
        'description': 'مبل با کیفیت بالا و طراحی مدرن برای پذیرایی شما. ساخته شده از بهترین چوب گردو و پارچه‌های مرغوب ایتالیایی.',
        'url': 'https://example.com/sofa',
        'expiry_date': timezone.now() + timedelta(days=30),  # ۳۰ روز بعد
    },
    {
        'title': 'سامسونگ گلکسی S24 Ultra',
        'description': 'گوشی هوشمند با دوربین ۲۰۰ مگاپیکسلی، باتری قدرتمند و صفحه‌نمایش AMOLED با کیفیت بین‌نظیر.',
        'url': 'https://example.com/samsung',
        'expiry_date': timezone.now() + timedelta(days=45),  # ۴۵ روز بعد
    },
    {
        'title': 'کپسول آتشنشانی ۶ کیلویی',
        'description': 'تجهیزات ایمنی با استاندارد جهانی برای محیط کار و منزل. دارای گواهی ISO 9001 و ضمانت ۵ ساله.',
        'url': 'https://example.com/fire-extinguisher',
        'expiry_date': timezone.now() + timedelta(days=60),  # ۶۰ روز بعد
    },
    {
        'title': 'دوره آموزش بازاریابی دیجیتال',
        'description': 'دوره جامع و کاربردی بازاریابی دیجیتال با تدریس اساتید مجرب. مناسب برای صاحبان کسب‌وکار و مدیران بازاریابی.',
        'url': 'https://example.com/digital-marketing',
        'expiry_date': timezone.now() + timedelta(days=90),  # ۹۰ روز بعد
    }
]


print("=" * 60)
print("🚀 شروع بارگذاری داده‌های نمونه...")
print("=" * 60)

created_count = 0
existing_count = 0

for data in ads_data:
    if not Advertisement.objects.filter(title=data['title']).exists():
        try:
            ad = Advertisement.objects.create(
                title=data['title'],
                description=data['description'],
                url=data['url'],
                is_active=True,
                views_count=random.randint(0, 100),
                expiry_date=data['expiry_date']  # ✅ اضافه شد
            )
            # ایجاد تصویر ساختگی
            img = create_dummy_image(data['title'])
            ad.image_name.save(f"{data['title'][:30]}.jpg", img, save=True)
            created_count += 1
            print(f"✅ {data['title']} ایجاد شد (انقضا: {data['expiry_date'].strftime('%Y-%m-%d')})")
        except Exception as e:
            print(f"❌ خطا در ایجاد {data['title']}: {e}")
    else:
        existing_count += 1
        print(f"⚠️ {data['title']} قبلاً وجود دارد")

print("=" * 60)
print(f"📊 گزارش نهایی:")
print(f"✅ ایجاد شده: {created_count}")
print(f"⚠️ موجود قبلی: {existing_count}")
print("=" * 60)

# نمایش لیست تبلیغات موجود
print("\n📋 لیست تبلیغات موجود در دیتابیس:")
print("-" * 60)
ads = Advertisement.objects.all()
for ad in ads:
    expiry_status = "✅ معتبر" if not ad.is_expired() else "⛔ منقضی"
    print(f"{ad.id}. {ad.title[:40]}... | بازدید: {ad.views_count} | {expiry_status}")
print("=" * 60)
print("✅ فرآیند Seed با موفقیت به پایان رسید!")
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Blog

class BlogSitemap(Sitemap):
    changefreq = 'weekly'  # هر هفته یکبار
    priority = 0.7  # اولویت بالا

    def items(self):
        return Blog.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.register_data  # تاریخ آخرین به‌روزرسانی

    def location(self, obj):
        return reverse('blogs:post_blog', args=[str(obj.id)])
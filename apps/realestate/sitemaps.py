# apps/products/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, ProductGroup

class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return reverse("realestate:product_details", kwargs={"slug": obj.slug})

class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return ProductGroup.objects.filter(is_active=True)

    # ====== اصلاح این خط ======
    def location(self, obj):
        return reverse("realestate:product_of_group", kwargs={"slug": obj.slug})
        #                       ^^^^^^^^^^^^^^^^ اینجا را اصلاح کن

class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['main:home', 'main:about_us', 'main:sliders','main:regulations','main:realestate','main:index','main:shop']

    def location(self, item):
        return reverse(item)
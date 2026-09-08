from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from apps.main.views import home  
from django.http import HttpResponse
from django.conf import settings
from django.contrib import admin
import os
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from apps.products.sitemaps import ProductSitemap, CategorySitemap, StaticViewSitemap
from apps.blog.sitemaps import BlogSitemap 
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from apps.products.sitemaps import ProductSitemap, CategorySitemap, StaticViewSitemap
sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'blogs': BlogSitemap,
    'static': StaticViewSitemap,}


# ===== ویوی مخصوص فایل تأیید اینماد =====
def txt_file_view(request):
    # استفاده از settings.BASE_DIR (روش اول)
    file_path = os.path.join(settings.BASE_DIR, '33476952.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return HttpResponse(f.read(), content_type='text/plain')
    else:
        return HttpResponse("File not found", status=404)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.main.urls',namespace='main')),
    path('accounts/',include('apps.accounts.urls',namespace='accounts')),
    path('products/',include('apps.products.urls',namespace='products')),
    path('realestate/',include('apps.realestate.urls',namespace='realestate')),
    path('orders/',include('apps.orders.urls',namespace='orders')),
    path('discounts/',include('apps.discounts.urls',namespace='discounts')),
    path('payments/',include('apps.payments.urls',namespace='payments')),
    path('warehouses/',include('apps.warehouses.urls',namespace='warehouses')),
    path('csf/',include('apps.comment_scoring_favorites.urls',namespace='csf')),
    path('search/',include('apps.search.urls',namespace='search')),
    path('blogs/',include('apps.blog.urls',namespace='blogs')),
    path('advertisements/',include('apps.advertisement.urls',namespace='advertisements')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('chatbot/', include('apps.chatbot.urls')),
    path('emailer/', include('apps.emailer.urls')),
    # path('test_api/', include('apps.test_api.urls',namespace='test_api')),
    path('specialties/', include('apps.specialties.urls',namespace='specialties')),
    path('support/', include('apps.support.urls',namespace='support')),
    # path("django-check-seo/", include("django_check_seo.urls")),
    path('33476952.txt', txt_file_view, name='verify_file'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    
 ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

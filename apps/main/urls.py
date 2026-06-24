from django.urls import path
from .views import index,SliderView,shop,realestate,AboutUsView,create_post,regulations
#----------------------------------------------------------------
app_name = 'main'
urlpatterns = [
    path('',index,name='index'),
    path('shop/',shop,name='shop'),
    path('realestate/',realestate,name='realestate'),
    path('about_us/',AboutUsView.as_view(),name='about_us'),
    path('sliders/',SliderView.as_view(),name='sliders'),
    path ('add/',create_post,name='PostCreate'),
    path ('regulations/',regulations, name='regulations'),
    
]
# chench the test

from django.urls import path  
from .views import advertisement_list 
app_name= 'advertisements'
urlpatterns = [  
    path('advertisements/', advertisement_list, name='advertisement_list'),  
  
]
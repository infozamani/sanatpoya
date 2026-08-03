from django.urls import path  
from .views import advertisement_list ,advertisement_create
app_name= 'advertisements'
urlpatterns = [  
    path('advertisements/', advertisement_list, name='advertisement_list'), 
    path('advertisement_create/', advertisement_create, name='advertisement_create'), 
  
]
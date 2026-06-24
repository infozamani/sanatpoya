from django.urls import path  
from .views import chat_view  

urlpatterns = [  
    path('chat/<str:shop>/', chat_view, name='chat'),  
]
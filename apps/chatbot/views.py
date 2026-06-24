
from django.shortcuts import render  

def chat_view(request, shop):  
    return render(request, 'chatbot/chat.html', {  
        'shop': shop  
    })
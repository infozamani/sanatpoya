# ================================================================
# teams/views.py
# ================================================================
from django.shortcuts import render
from django.conf import settings
from .models import TeamMember

def team_list(request):
    """نمایش لیست تیم با اسلایدر"""
    
    # 1. اعضای ویژه (کارت بزرگ)
    featured_members = TeamMember.objects.filter(
        is_featured=True, 
        is_active=True
    ).order_by('order')[:2]
    
    # 2. اعضای عادی (برای اسلایدر)
    regular_members = list(
        TeamMember.objects.filter(
            is_featured=False, 
            is_active=True
        ).order_by('order')
    )
    
    # 3. تقسیم به گروه‌های ۲ تایی برای اسلایدر
    grouped_members = []
    for i in range(0, len(regular_members), 2):
        grouped_members.append(regular_members[i:i+2])
    
    # 4. اگر اعضای عادی وجود نداشت، از اعضای ویژه استفاده کن (با is_featured=False)
    if not regular_members and featured_members:
        # همه اعضا را به عنوان عادی در نظر بگیر
        all_members = list(TeamMember.objects.filter(is_active=True).order_by('order'))
        for i in range(0, len(all_members), 2):
            grouped_members.append(all_members[i:i+2])
        featured_members = []  # اعضای ویژه را خالی کن
    
    context = {
        'featured_members': featured_members,
        'grouped_members': grouped_members,
        'has_slider': len(grouped_members) > 1,  # اگر بیش از 1 اسلاید باشد
        'media_url': settings.MEDIA_URL,
    }
    return render(request, 'team_app/team.html', context)
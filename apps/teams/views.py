from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import TeamMember

def team_list(request):
    """View for listing all team members"""
    # دریافت اعضای ویژه (Featured) - کارت‌های بزرگ
    featured_members = TeamMember.objects.filter(is_featured=True, is_active=True).order_by('order')[:2]
    
    # دریافت سایر اعضا - کارت‌های جمع و جور
    regular_members = TeamMember.objects.filter(is_featured=False, is_active=True).order_by('order')
    
    context = {
        'featured_members': featured_members,
        'regular_members': regular_members,
        'all_members': TeamMember.objects.filter(is_active=True).order_by('order'),
        'media_url': settings.MEDIA_URL,
    }
    return render(request, 'team_app/team.html', context)


# def team_member_detail(request, pk):
#     """View for single team member details"""
#     member = get_object_or_404(TeamMember, pk=pk, is_active=True)
    
#     context = {
#         'member': member,
#         'media_url': settings.MEDIA_URL,
#     }
#     return render(request, 'teams/member_detail.html', context)
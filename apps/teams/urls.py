from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.team_list, name='team_list'),
    # path('<int:pk>/', views.team_member_detail, name='team_member_detail'),
]
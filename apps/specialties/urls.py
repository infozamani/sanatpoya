from django.urls import path
from . import views

app_name = 'specialties'
urlpatterns = [
    path ('popular_expert_groups/',views.get_popular_expert_groups,name='popular_expert_groups'),
    path ('expert_details/<slug:slug>/',views.ExpertDetaileView.as_view(),name='expert_details'),
    path ('related_experts/<slug:slug>/',views.get_related_experts,name='related_experts'),
    path ('expert_groups/',views.ExpertGroupView.as_view(),name='expert_groups'),
    path ('expert_of_group/<slug:slug>/',views.ExpertsBygroupView.as_view(),name='expert_of_group'),
    path ('ajax_admin/',views.get_filter_value_for_feature,name='filter_value_for_feature'),
    path ('expert_groups_partial/',views.get_expert_groups,name='expert_groups_partial'),
    # path ('ProductsBygroup/<slug:slug>/',views.ExpertsBygroupView.as_view(),name='ProductsBygroup'),
    path ('identitys_partial/<slug:slug>/',views.get_identitys,name='identitys_partial'),
    path ('ability_partial/<slug:slug>/',views.get_abilitys,name='ability_partial'),
    path ('fieldwork_partial/<slug:slug>/',views.get_fieldworks,name='fieldwork_partial'),
    path ('service_partial/<slug:slug>/',views.get_services,name='service_partial'),
    path ('checkout_expert/<int:expert_id>/',views.CheckoutExpertView.as_view(), name='checkout_expert'),

]

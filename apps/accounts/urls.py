from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path ('register/',RegisterUserView.as_view(),name='register'),
    path ('verify/',VerifyRegisterCodeView.as_view(),name='verify'),
    path ('login/',loginUserView.as_view(),name='login'),
    path ('login_shop/',loginUserView.as_view(),name='login_shop'),
    path ('logout/',LogoutUserView.as_view(),name='logout'),
    path ('change_pass/',ChangePasswordView.as_view(),name='change_pass'),
    path ('remember_pass/',RememberPasswordView.as_view(),name='remember_pass'),
    path ('userpanel/',UserPanelView.as_view(),name='userpanel'),
    path ('userpanelexpert/',UserPaneExpertlView.as_view(),name='userpanel_expert'),
    path ('update-profile/',UpdateProfileView.as_view(),name='update-profile'),
    path ('show_last_orders/',show_last_orders,name='show_last_orders'),
    # path ('show_last_experts/',show_last_orders,name='show_last_experts'),
    path ('show_user_payments/',show_user_payments,name='show_user_payments'),
     
]

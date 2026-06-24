from django.urls import path
from .views import CommantView,add_score,add_scoreexpert ,UserFavoriteView,add_to_favorite,CommantExpertView
 

app_name = 'csf'
urlpatterns = [
    path('create_comment/<slug:slug>/', CommantView.as_view(), name='create_comment'),
    path('create_commentexpert/<slug:slug>/', CommantExpertView.as_view(), name='create_commentexpert'),
    # path ('add_to_favorite/',add_to_product_fvorite, name='add_to_favorite'),
    path('add_score/', add_score, name='add_score'),
    path('add_scoreexpert/', add_scoreexpert, name='add_scoreexpert'),
    path('add_to_favorite/', add_to_favorite, name='add_to_favorite'),
    path('user_favorite/', UserFavoriteView.as_view(), name='user_favorite'),
    

]
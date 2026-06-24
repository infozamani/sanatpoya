from django.contrib import admin
from .models import Comment,Favorite,CommentExpert
#----------------------------------------------------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'commenting_user', 'comment_text' ,'is_active')
    list_editable = ['is_active']
@admin.register(Favorite)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'favorite_user', 'registerdate'  )
#----------------------------------------------------------------
@admin.register(CommentExpert)
class CommentExpertAdmin(admin.ModelAdmin):
    list_display = ('expert', 'commenting_user', 'comment_text' ,'is_active')
    list_editable = ['is_active']
 
    
    

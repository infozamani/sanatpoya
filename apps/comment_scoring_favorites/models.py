from django.db import models 
from apps.products.models import Product
from apps.accounts.models import CustomUser
from django.core.validators import MinLengthValidator, MaxValueValidator
from apps.specialties.models import Expert
#----------------------------------------------------------------
## create a comment for a product
class Comment(models.Model):
    product = models.ForeignKey(Product, verbose_name="کالا",related_name='comments_product', on_delete=models.CASCADE)
    commenting_user = models.ForeignKey(CustomUser, verbose_name="کاربر نظر دهنده",related_name='approving_user1', on_delete=models.CASCADE)
    approving_user = models.ForeignKey(CustomUser, verbose_name="کاربر تایید کننده نظر",related_name='approving_user2', on_delete=models.CASCADE,null=True, blank=True)
    comment_text = models.TextField(max_length=200,verbose_name='متن نظر')
    registerdate = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت نظر')
    comment_parent = models.ForeignKey("Comment", verbose_name="والد نظر",null=True, blank=True, on_delete=models.CASCADE, related_name='comments_child')

    def __str__(self) -> str:
        return f"{self.product} - {self.commenting_user}"
   
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
#----------------------------------------------------------------
## create a commentexpert for a product
class CommentExpert (models.Model):
    expert = models.ForeignKey(Expert, verbose_name="متخصص",related_name='comments_expert', on_delete=models.CASCADE)
    commenting_user = models.ForeignKey(CustomUser, verbose_name="کاربر نظر دهنده",related_name='approving_user3', on_delete=models.CASCADE)
    approving_user = models.ForeignKey(CustomUser, verbose_name="کاربر تایید کننده نظر",related_name='approving_user4', on_delete=models.CASCADE,null=True, blank=True)
    comment_text = models.TextField(max_length=200,verbose_name='متن نظر')
    registerdate = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت نظر')
    comment_parent = models.ForeignKey("CommentExpert", verbose_name="والد نظر",null=True, blank=True, on_delete=models.CASCADE, related_name='comments_child')

    def __str__(self) -> str:
        return f"{self.expert} - {self.commenting_user}"
   
    class Meta:
        verbose_name = 'نظرمتخصص'
        verbose_name_plural = 'نظرات متخصصین'
#----------------------------------------------------------------
## create  a class scoring for the score 
class Scoring(models.Model):
    product = models.ForeignKey(Product, verbose_name="کالا",related_name='scoring_product', on_delete=models.CASCADE)
    scoring_user = models.ForeignKey(CustomUser, verbose_name="کاربر امتیاز دهنده",related_name='scoring_user1', on_delete=models.CASCADE)
    registerdate = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')        
    score = models.PositiveIntegerField(verbose_name=('امتیاز'),validators=[MinLengthValidator(0),MaxValueValidator(5)])
    
    def __str__(self) -> str:
        return f"{self.product} - {self.scoring_user}"

    class Meta:
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیازات'
#----------------------------------------------------------------
## create  a class scoring for the score 
class ScoringExpert(models.Model):
    expert = models.ForeignKey(Expert, verbose_name="کالا",related_name='scoring_expert', on_delete=models.CASCADE)
    scoring_user = models.ForeignKey(CustomUser, verbose_name="کاربر امتیاز دهنده",related_name='scoring_user', on_delete=models.CASCADE)
    registerdate = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')        
    score_exp = models.PositiveIntegerField(verbose_name=('امتیاز'),validators=[MinLengthValidator(0),MaxValueValidator(5)])
    
    def __str__(self) -> str:
        return f"{self.expert} - {self.scoring_user}"

    class Meta:
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیازات'
        
#----------------------------------------------------------------
## create a new class favorite
class Favorite(models.Model):
    product = models.ForeignKey(Product, verbose_name="کالا",related_name='favorite_product', on_delete=models.CASCADE)  
    favorite_user = models.ForeignKey(CustomUser, verbose_name="کاربر علاقه مند ",related_name='favorite_user1', on_delete=models.CASCADE)
    registerdate = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
        
    def __str__(self) -> str:
        return f"{self.product} - {self.favorite_user} - {self.registerdate}"

    class Meta:
        verbose_name = 'علاقه'
        verbose_name_plural = 'علایق'
                                
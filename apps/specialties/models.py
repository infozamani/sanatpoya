from django.db import models
from utils import FileUpload
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.html import mark_safe
from apps.accounts.models import Customer,CustomUser
from middlewares.middlewares import RequestMiddleware
from django.db.models import Sum,Avg
from django.core.validators import MinLengthValidator, MaxValueValidator
# Create your models here.

#------------------------------------------------------------------------
## create class Identity
class Identity (models.Model):
    identity_name = models.CharField( max_length=100, verbose_name='حقیقی/حقوقی ')
    slug =  models.SlugField(max_length=200,null=True)
    
    def __str__(self) -> str:
        return self.identity_name
    class Meta:
        verbose_name = 'شخص'
        verbose_name_plural = 'اشخاص'
#------------------------------------------------------------------------
## create class ability
class Ability (models.Model):
    ability_name = models.CharField( max_length=100, verbose_name='نوع توانمندی ')
    slug =  models.SlugField(max_length=200,null=True)
    
    def __str__(self) -> str:
        return self.ability_name
    class Meta:
        verbose_name = 'توانمندی'
        verbose_name_plural = 'توانمندی ها'
#------------------------------------------------------------------------
## create class fieldwork
class FieldWork (models.Model):
    fieldwork_name = models.CharField( max_length=100, verbose_name='زمینه فعالیت  ')
    slug =  models.SlugField(max_length=200,null=True)
    
    def __str__(self) -> str:
        return self.fieldwork_name
    class Meta:
        verbose_name = 'زمینه'
#------------------------------------------------------------------------
## create class Services
class Services(models.Model):
    service_name = models.CharField( max_length=100, verbose_name='نوع خدمات  ')
    slug =  models.SlugField(max_length=200,null=True)
    
    def __str__(self) -> str:
        return self.service_name
    class Meta:
        verbose_name = 'خدمات'
        verbose_name_plural = ' نوع خدمات'
        verbose_name_plural = 'زمینه فالیت ها  '
    
#------------------------------------------------------------------------
## create class Capabilities group
class ExpertiseGroup (models.Model):
    group_title = models.CharField(max_length=500, verbose_name='عناوین تخصص')
    file_upload = FileUpload('images', 'ExpertiseGroup')
    image_name = models.ImageField(upload_to = file_upload.upload_to, verbose_name=' تصویر گروه تخصص') 
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True,blank=True, verbose_name='وضعیت فعال /غیر فعال')
    group_parent = models.ForeignKey("ExpertiseGroup", verbose_name="والد گروه تخصص", on_delete=models.CASCADE, blank=True, null=True,related_name = 'groups_parent') 
    register_date = models.DateTimeField(verbose_name=("تاریخ درج"), auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True, verbose_name='آخرین بروز رسانی تخصص')
    slug =  models.SlugField(max_length=200,unique=True)
    
    def __str__(self) -> str:
        return self.group_title
    class Meta:
        verbose_name = 'گروه تخصص'
        verbose_name_plural = ' گروه تخصص ها'
# #------------------------------------------------------------------------
# ## create class Feature(ویژگیها)
class Feature(models.Model):
    feature_name = models.CharField(verbose_name=("نام ویژگی تخصص"), max_length=100)
    expert_group = models.ManyToManyField(ExpertiseGroup, verbose_name=("گروه تخصص"), related_name = 'Features_of_groups')
 
    class Meta:
        verbose_name = (" ویژگی تخصص" )
        verbose_name_plural =(" انواع عملگرها تخصص")  

    def __str__(self):
        return self.feature_name

        


#---------------------------------------------------------------------------------------------
## create class Expert
class Expert(models.Model):
    expert_user = models.ForeignKey(Customer, verbose_name="کاربر",related_name='experts_user', on_delete=models.CASCADE)
    expert_customuser = models.ForeignKey(CustomUser,max_length=11,blank= None,verbose_name='شماره موبایل ' , on_delete=models.CASCADE)
    summery_description = models.TextField(default="",blank=True, null=True, verbose_name=' توضیحات کوتاه')
    description = RichTextUploadingField(config_name = 'special',blank= None)
    file_upload = FileUpload('images', 'Expert')
    image_name = models.ImageField(upload_to = file_upload.upload_to, verbose_name=' تصویر  متخصص')
    ostan = models.CharField( max_length=50,verbose_name='استان' )
    is_active = models.BooleanField(default=True,blank=True, verbose_name='وضعیت فعال /غیر فعال')
    subscription = models.BooleanField(default=True,blank=True, verbose_name='اشتراک فعال /غیر فعال')
    register_date = models.DateTimeField( auto_now_add=True,verbose_name=("تاریخ درج"),)
    published_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    update_date = models.DateTimeField(auto_now=True, verbose_name='آخرین بروز رسانی متخصص')
    expertise_group = models.ManyToManyField(ExpertiseGroup, verbose_name=("گروه متخصص"), related_name = 'expertises_of_group')
    identity = models.ForeignKey(Identity,  on_delete=models.CASCADE, related_name='identity',verbose_name=("نوع اشخاص"))
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE,related_name='ability',verbose_name="نوع توانمندی" )
    fieldwork = models.ForeignKey(FieldWork, on_delete=models.CASCADE, related_name='fieldwork',verbose_name="   زمینه کاری")
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='service',verbose_name="      نوع خدمات", )
    degree = models.CharField(verbose_name='آخرین مدرک تحصیلی', max_length=50)  
    slug = models.SlugField(max_length=200,null=True)

    def __str__(self):
        return f"{self.expert_user}"
    class Meta:
        verbose_name = ("متخصص")
        verbose_name_plural =("متخصص ها")
        
    def get_absolute_url(self):
        return reverse("specialties:expert_details", kwargs={"slug":self.slug})
     #--------------------------------------
    ## some scores are for any production that is  having user 
    def get_user_score_exp(self):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        score = 0
        user_score = self.scoring_expert.filter(scoring_user=request.user)
        if user_score.count()>0:
            score = user_score[0].score_exp
             
        return score 
        #--------------------------------------
    ## create avg function for any product with score
    def get_average_score_exp(self):
        avgScore = self.scoring_expert.all().aggregate(Avg('score_exp'))['score_exp__avg']
        if avgScore == None :
            avgScore = 0
        return avgScore

#---------------------------------------------------------------------------------------------
## create class FeatureValue
class FeatureExpertValue(models.Model):
    value_title = models.CharField(max_length=50, verbose_name=' جنس ویژگی تخصص')
    feature = models.ForeignKey(Feature, verbose_name=("نام ویژگی تخصص"), on_delete=models.CASCADE, related_name='feature_value')

    def __str__(self):
        return f"{self.id}  {self.value_title}"
    class Meta:
        verbose_name = ("نوع تخصص ")
        verbose_name_plural =("ماهیت های ویژگی تخصص   ")

#---------------------------------------------------------------------------------------------
## create class productFeature
class ExpertFeature(models.Model):
    expert = models.ForeignKey(Expert, verbose_name=(" نام تخصص "), on_delete=models.CASCADE,related_name='Expert_features')
    feature = models.ForeignKey(Feature, verbose_name=("نام ویژگی تخصص"), on_delete=models.CASCADE)
    value = models.CharField( max_length=100, verbose_name='نوع  ویژکی تخصص')
    filter_value = models.ForeignKey(FeatureExpertValue, null=True, blank=True, verbose_name="مقدار ویژگی برای فیلتر", on_delete=models.CASCADE,)
    def __str__(self) -> str:
        return f"{self.expert}  - {self.feature} : {self.value}" 
    class Meta:
        verbose_name = ("ویژکی تخصص")
        verbose_name_plural =("ویژگی های تخصص ها")  
        #---------------------------------------------------------------------------------------------
## create class productGallery
class ExpertGallery(models.Model):
    product = models.ForeignKey(Expert, verbose_name=("متخصص"), on_delete=models.CASCADE,related_name='gallery_product')
    file_upload = FileUpload('images', 'ExpertiseGroup')
    image_name = models.ImageField(upload_to = file_upload.upload_to, verbose_name=' تصویر  متخصص')
    class Meta:
        verbose_name = ("تصویر ")
        verbose_name_plural =('تصاویر')
  

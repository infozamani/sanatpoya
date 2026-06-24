from django.db import models  
from utils import FileUpload

class Advertisement(models.Model):  
    title = models.CharField(max_length=100,verbose_name='عنوان تبلیغ')  
    description = models.TextField(verbose_name='توضیحات تبلیغ')  
    file_upload = FileUpload('images', 'advertisement')
    image_name = models.ImageField(upload_to = file_upload.upload_to, verbose_name=' تصویر   تبلیغات')
    url = models.URLField(max_length=200, verbose_name='لینک ')  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):  
        return self.title
from django.db import models

class TeamMember(models.Model):
    """Model for team members displayed on the site"""
    name = models.CharField(max_length=100, verbose_name="نام کامل")
    role = models.CharField(max_length=100, verbose_name="سمت")
    bio = models.TextField(blank=True, null=True, verbose_name="بیوگرافی")
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="تلفن")
    
    # مدارک و گواهی‌ها (به صورت لیست JSON)
    credentials = models.JSONField(default=list, verbose_name="مدارک و گواهی‌ها")
    # مثال: ["PMP Certified", "OSHA 30", "Licensed Contractor"]
    
    # مهارت‌ها (به صورت لیست JSON)
    skills = models.JSONField(default=list, verbose_name="مهارت‌ها")
    # مثال: ["PE License", "LEED AP", "Project Management"]
    
    # لینک‌های شبکه‌های اجتماعی
    linkedin = models.URLField(blank=True, null=True, verbose_name="LinkedIn")
    twitter = models.URLField(blank=True, null=True, verbose_name="Twitter")
    facebook = models.URLField(blank=True, null=True, verbose_name="Facebook")
    instagram = models.URLField(blank=True, null=True, verbose_name="Instagram")
    
    # تصویر پروفایل
    photo = models.ImageField(upload_to='team/', blank=True, null=True, verbose_name="عکس")
    
    # سابقه کاری (سال‌ها تجربه)
    experience_years = models.IntegerField(default=0, verbose_name="سال‌های تجربه")
    
    # ترتیب نمایش و وضعیت
    order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    is_featured = models.BooleanField(default=False, verbose_name="نمایش ویژه (کارت بزرگ)")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return self.name
    
    def get_credentials_list(self):
        """بازگرداندن لیست مدارک"""
        if isinstance(self.credentials, list):
            return self.credentials
        elif isinstance(self.credentials, dict):
            return list(self.credentials.values())
        return []
    
    def get_skills_list(self):
        """بازگرداندن لیست مهارت‌ها"""
        if isinstance(self.skills, list):
            return self.skills
        elif isinstance(self.skills, dict):
            return list(self.skills.values())
        return []
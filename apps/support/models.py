from django.db import models
from django.conf import settings  # Import the settings module
 
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'باز'),
        ('closed', 'بسته'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Update to use AUTH_USER_MODEL
    support_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')  # Update to use AUTH_USER_MODEL
    
    def __str__(self):
        return self.title

class TicketReply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Update to use AUTH_USER_MODEL
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True,verbose_name='فعال/غیرفعال')

    def __str__(self):
        return f"Reply by {self.user } on {self.created_at}"

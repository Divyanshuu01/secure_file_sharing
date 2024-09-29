from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('operation', 'Operation User'),
        ('client', 'Client User'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

class File(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='uploads/', blank=False, null=False)
    allowed_types = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # docx
                     'application/vnd.openxmlformats-officedocument.presentationml.presentation',  # pptx
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']  # xlsx
    uploaded_at = models.DateTimeField(auto_now_add=True)

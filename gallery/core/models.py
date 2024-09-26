from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    
    def __str__(self):
        return self.username
    
class Gallery(models.Model):
    gallery_name = models.CharField(max_length=300)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.gallery_name
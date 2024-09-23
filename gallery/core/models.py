from django.db import models

# Create your models here.
class Gallery(models):
    gallery_name = models.CharField(max_length=300)
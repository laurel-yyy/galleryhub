from django.db import models

# Create your models here.
class Gallery(models.Model):
    gallery_name = models.CharField(max_length=300)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.gallery_name
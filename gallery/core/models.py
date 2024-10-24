from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    
    def __str__(self):
        return self.username


class Gallery(models.Model):
    gallery_name = models.CharField(max_length=300, primary_key=True)
    location = models.CharField(max_length=50)
    description = models.TextField(default="gallery description")
    image = models.ImageField(upload_to='img/gallery', default='img/gallery/default.jpg')
    visitor_capacity = models.IntegerField(default=300)
    rating = models.FloatField(default=3.0)

    def __str__(self):
        return self.gallery_name


class Author(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description  =  models.TextField(default="Author description")
    rating = models.FloatField(default=3.0)

    
    def __str__(self):
        return self.name


class Artwork(models.Model):
    title = models.CharField(max_length=50, primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="artwork")
    description = models.TextField(default="artwork description")
    gallery = models.ForeignKey(Gallery,  on_delete=models.CASCADE, related_name="artwork")
    image = models.ImageField(upload_to='img/artwork')
    rating = models.FloatField(default=3.0)
    year = models.PositiveIntegerField(default=2000)

    def __str__(self):
        return self.title


class StyleTag(models.Model):
    tag_name = models.CharField(max_length=50, primary_key=True)
    artwork = models.ManyToManyField(Artwork, related_name="styletag")
    description = models.TextField(default="styletag description")

    def __str__(self):
        return self.tag_name


class ReservationOrder(models.Model):
    user_name =  models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reservation")
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name="reservation")
    created_time = models.TimeField(auto_now_add=True)
    order_date = models.DateField()

    def __str__(self):
        return self.user_name + ' ' + self.gallery + ' ' + self.created_time

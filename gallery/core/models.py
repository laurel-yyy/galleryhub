from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.db.models import Subquery, OuterRef, Avg

import uuid


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
    
    def get_comments(self):
        return Comment.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk
        )


class Author(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description  =  models.TextField(default="Author description")
    rating = models.FloatField(default=3.0)
    
    def __str__(self):
        return self.name
    
    def get_comments(self):
        return Comment.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk
        )        


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
    
    def get_comments(self):
        return Comment.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk
        ) 



class StyleTag(models.Model):
    tag_name = models.CharField(max_length=50, primary_key=True)
    artwork = models.ManyToManyField(Artwork, related_name="styletag")
    description = models.TextField(default="styletag description")

    def __str__(self):
        return self.tag_name


class ReservationOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name =  models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reservation")
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name="reservation")
    created_time = models.TimeField(auto_now_add=True)
    order_date = models.DateField()
    num_people = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.user_name} - {self.gallery} - {self.order_date} - {self.created_time}"
    


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=300) 
    content_object = GenericForeignKey('content_type', 'object_id') 

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(default="the user hasn't made comment")
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    created_time = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} comment on {self.content_object} at {self.created_time}"
    
    def save(self, *args, **kwargs):
        # if not self.id:
        #     self.id = f"{self.user.username}_{self.object_id}_{self.created_time}"
        super().save(*args, **kwargs)


# update rating
@receiver(post_save, sender=Comment)
@receiver(post_delete, sender=Comment)
def update_object_average_rating(sender, instance, **kwargs):
    latest_comment_ids = Comment.objects.filter(
        content_type=instance.content_type,
        object_id=instance.object_id,
        rating__isnull=False,
        user=OuterRef('user')
    ).order_by('-created_time').values('id')[:1]

    latest_ratings = Comment.objects.filter(
        id__in=Subquery(latest_comment_ids)
    )
    average_rating = latest_ratings.aggregate(Avg('rating'))['rating__avg']

    content_object = instance.content_object
    content_object.rating = average_rating if average_rating is not None else 4.0
    content_object.save()

# update styletag
@receiver(pre_delete, sender=Artwork)
def remove_artwork_from_styletags(sender, instance, **kwargs):
    for tag in instance.styletag.all():
        tag.artwork.remove(instance)
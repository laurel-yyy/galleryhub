from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Gallery, CustomUser, Author, Artwork, StyleTag, ReservationOrder, Comment
# Register your models here.

admin.site.register(Gallery)
admin.site.register(CustomUser)
admin.site.register(Author)
admin.site.register(Artwork)
admin.site.register(StyleTag)
admin.site.register(ReservationOrder)
admin.site.register(Comment)
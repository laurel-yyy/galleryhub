from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('page/', views.different_view_example, name="page" ),
    path('manage/gallery/<str:gallery_name>/', views.edit_gallery, name='edit_gallery'),
    path('manage/gallery/<str:gallery_name>/artwork/add/', views.add_artwork_view, name='add_artwork'),
    path('manage/gallery/<str:gallery_name>/artwork/<str:artwork_title>/', views.edit_artwork_view, name='edit_artwork'),

    #path('manage/gallery/<str:gallery_name>/artwork/add/', views.add_artwork_view, name='add_artwork'),
    path('manage/author/add/', views.add_author_view, name='add_author'),
    path('manage/styletag/add/', views.add_styletag_view, name='add_styletag'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
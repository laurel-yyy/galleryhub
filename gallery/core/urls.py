from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    
    # path for login, logout and register
    path('register/', views.register, name="register"),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('page/', views.different_view_example, name="page" ),
    
    # path for gallery browse
    path('museum/', views.museum, name='museum'),
    path('gallery/<str:gallery_name>/', views.gallery_view, name='gallery'),
    path('styletag/<str:tag_name>/', views.styletag_detail, name='styletag_detail'),
    path('gallery/<str:gallery_name>/<str:artwork_title>/', views.artwork, name='artwork'),
    path('author/<str:author_name>/', views.author, name='author'),

    # path for admin pages
    path('manage/gallery/<str:gallery_name>/', views.edit_gallery, name='edit_gallery'),
    path('manage/gallery/<str:gallery_name>/artwork/add/', views.add_artwork_view, name='add_artwork'),
    path('manage/gallery/<str:gallery_name>/artwork/<str:artwork_title>/', views.edit_artwork_view, name='edit_artwork'),
    path('manage/author/add/', views.add_author_view, name='add_author'),
    path('manage/styletag/add/', views.add_styletag_view, name='add_styletag'),

    # path for reservation
    path('reservation/createorder/', views.create_reservation, name='create_reservation'),
    path('get_reservations_count/', views.get_reservations_count, name='get_reservations_count'),
    path('reservation/myreservations/', views.view_my_reservation, name='my_reservation'),
    path('get_weather_forecast/', views.get_weather_forecast, name='get_weather_forecast'),

    # path for search
    path('search/', views.search, name='search'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
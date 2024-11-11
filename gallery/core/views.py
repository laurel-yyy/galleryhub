from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.urls import reverse
from django.forms import modelformset_factory
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Gallery, Artwork, Author, StyleTag, ReservationOrder
from .forms import CustomUserCreationForm, GalleryForm, ArtworkForm, ArtworkFormSet, AuthorForm, StyleTagForm, ReservationOrderForm
from django.http import HttpResponse
from django.template import loader
from django.db.models import Sum
from datetime import date


# Create your views here.

def home(request):
    """
    Renders the homepage template.
    """
    return render(request, 'home.html')

def museum(request):
    galleries = Gallery.objects.all()
    return render(request, 'museum.html', {'galleries': galleries} )


def register(request):
    """
    Handles user registration. If the method is POST and the form is valid,
    a new user is created, logged in, and redirected to the homepage.
    If the method is GET, it renders the registration form.
    """
    if request.method == 'POST':
        register_form = CustomUserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            messages.success(request, 'Register Suceed!')
            return redirect('home')
    else:
        register_form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': register_form})


@login_required
def different_view_example(request):
    """
    An example for render different view to user and admin
    """
    if request.user.is_staff:
        return render(request, 'admin_page.html')
    else:
        return render(request, 'user_page.html')


# Views for admin 

@login_required
def edit_gallery(request, gallery_name):
    """
    Handles the editing of a gallery. Retrieves the gallery instance based on
    the name, and allows the user to edit the gallery and associated artworks.
    On successful POST, saves the changes and redirects back to the edit page.
    """
    if not request.user.is_staff:
        return redirect('home')
    
    gallery = get_object_or_404(Gallery, gallery_name=gallery_name)
    
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=gallery)
        #formset = ArtworkFormSet(request.POST, request.FILES, instance=gallery)

        if form.is_valid():
            form.save()
            #formset.save()
            return redirect('edit_gallery', gallery_name=gallery.gallery_name)
    else:
        form = GalleryForm(instance=gallery)
        formset = ArtworkFormSet(instance=gallery)

    return render(request, 'edit_gallery.html', {
        'form': form, 
        'gallery': gallery
    })


@login_required
def edit_artwork_view(request, gallery_name, artwork_title):
    """
    Handles the editing of a specific artwork. Retrieves the artwork based on the title
    and its associated gallery. If the method is POST and the form is valid, updates the
    artwork and redirects to the gallery edit page.
    """

    if not request.user.is_staff:
        return redirect('home')

    gallery = get_object_or_404(Gallery, gallery_name=gallery_name)
    artwork = get_object_or_404(Artwork, title=artwork_title, gallery=gallery)

    if request.method == 'POST':

        if 'delete_artwork' in request.POST:
            artwork.delete()
            return redirect('edit_gallery', gallery_name=gallery.gallery_name)
        
        artwork_form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if artwork_form.is_valid():
            artwork_form.save()

            return redirect('edit_gallery', gallery_name=gallery.gallery_name)
    else:
        artwork_form = ArtworkForm(instance=artwork)

    return render(request, 'edit_artwork.html', {
        'artwork_form': artwork_form,
        'gallery': gallery,
        'artwork': artwork
    })


@login_required
def add_artwork_view(request, gallery_name):
    """
    Handles the creation of a new artwork for a specific gallery. If the method
    is POST and the form is valid, it saves the new artwork and redirects to the
    gallery edit page. If the method is GET, it displays a blank artwork form.
    """

    if not request.user.is_staff:
        return redirect('home')
    
    gallery = get_object_or_404(Gallery, gallery_name=gallery_name)
    
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_artwork = form.save(commit=False)
                new_artwork.gallery = gallery  
                new_artwork.save()
                form.save_m2m()  
                return redirect('edit_gallery', gallery_name=gallery.gallery_name)
            except IntegrityError:
                form.add_error(None, "There was an error saving the artwork. Please try again.")
    else:
        form = ArtworkForm()
    
    return render(request, 'add_artwork.html', {'form': form, 'gallery': gallery})


@login_required
def add_author_view(request):
    """
    Handles the creation of a new author. If the method is POST and the form is valid,
    it saves the new author and redirects to the previous page or the gallery edit page
    based on the request. If the method is GET, it displays the author creation form.
    """

    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            previous_url = request.META.get('HTTP_REFERER')
            return redirect(previous_url) if previous_url else redirect('edit_gallery', gallery_name=request.GET.get('gallery_name'))
    else:
        form = AuthorForm()

    return render(request, 'add_author.html', {'form': form})


@login_required
def add_styletag_view(request):
    """
    Handles the creation of a new style tag. If the method is POST and the form is valid,
    it saves the new style tag and redirects to the previous page or the gallery edit page
    based on the request. If the method is GET, it displays the style tag creation form.
    """
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = StyleTagForm(request.POST)
        if form.is_valid():
            form.save()
            previous_url = request.META.get('HTTP_REFERER')
            return redirect(previous_url) if previous_url else redirect('edit_gallery', gallery_name=request.GET.get('gallery_name'))
    else:
        form = StyleTagForm()

    return render(request, 'add_styletag.html', {'form': form})


def artwork(request, artwork_title):
    artworks = Artwork.objects.all().filter(title=artwork_title)
    template = loader.get_template('artwork.html')
    if len(artworks) == 0:
        return
    else:
        context = {
            'artwork':artworks[0],
        }
        return HttpResponse(template.render(context,request))

    
def author(request, author_name):
    author_found = Author.objects.all().filter(name=author_name)
    artworks = Artwork.objects.all().filter(author=author_name) 
    template = loader.get_template('author.html')
    if len(author_found) == 0:
        return
    else:
        context = {
            'author':author_found[0],
            'artworks':artworks,
        }
        return HttpResponse(template.render(context,request))


@login_required
def create_reservation(request):
    current_reservations = None
    capacity = None

    if request.method == 'POST':
        form = ReservationOrderForm(request.POST)
        if form.is_valid():
            gallery = form.cleaned_data['gallery']
            order_date = form.cleaned_data['order_date']
            num_people = form.cleaned_data['num_people']

            existing_reservation = ReservationOrder.objects.filter(
                user_name=request.user,
                order_date=order_date
            ).exists()

            if existing_reservation:
                form.add_error('order_date', 'You already have a reservation on this date.')
            else:
                current_reservations = ReservationOrder.objects.filter(
                    gallery=gallery,
                    order_date=order_date
                ).aggregate(total=Sum('num_people'))['total'] or 0
                capacity = gallery.visitor_capacity

                if current_reservations + num_people > capacity:
                    form.add_error(None, "Reservation Fail")
                else:
                    reservation = form.save(commit=False)
                    reservation.user_name = request.user
                    reservation.save()
                    return redirect('my_reservation')  
        
    else:
        form = ReservationOrderForm()

    return render(request, 'create_reservation.html', {
        'form':form,
        'current_reservations':current_reservations, 
        'capacity':capacity})


@login_required
def view_my_reservation(request):
    """
    Displays the logged-in user's reservations, separated by finished and upcoming ones,
    sorted by order date.
    """
    today = date.today()

    if request.method == 'POST' and 'delete_reservation_id' in request.POST:
        
        reservation_id = request.POST.get('delete_reservation_id')
        reservation = get_object_or_404(ReservationOrder, id=reservation_id, user_name=request.user)
        if reservation.order_date > today:
            reservation.delete()
            messages.success(request, 'Reservation deleted successfully.')
            return redirect('my_reservation')

    todays_reservations = ReservationOrder.objects.filter(
        user_name=request.user,
        order_date=today
    ).order_by('order_date')

    upcoming_reservations_list = ReservationOrder.objects.filter(
        user_name=request.user,
        order_date__gt=today
    ).order_by('order_date')

    finished_reservations_list = ReservationOrder.objects.filter(
        user_name=request.user,
        order_date__lt=today
    ).order_by('order_date')

    upcoming_paginator = Paginator(upcoming_reservations_list, 3)
    finished_paginator = Paginator(finished_reservations_list, 3)

    upcoming_page_number = request.GET.get('upcoming_page')
    finished_page_number = request.GET.get('finished_page')

    upcoming_reservations = upcoming_paginator.get_page(upcoming_page_number)
    finished_reservations = finished_paginator.get_page(finished_page_number)

    return render(request, 'my_reservations.html', {
        'todays_reservations': todays_reservations,
        'upcoming_reservations': upcoming_reservations,
        'finished_reservations': finished_reservations
    })

@login_required
def get_reservations_count(request):
    gallery_name = request.GET.get('gallery_name')
    order_date = request.GET.get('order_date')

    if gallery_name and order_date:
        gallery = Gallery.objects.get(gallery_name=gallery_name)
        current_reservations = ReservationOrder.objects.filter(
            gallery=gallery,
            order_date=order_date
        ).aggregate(total=Sum('num_people'))['total'] or 0
        capacity = gallery.visitor_capacity

        return JsonResponse({
            'current_reservations':current_reservations,
            'capacity':capacity
        })
    
    return JsonResponse({'error': 'Invalid data'}, status=400)

def get_weather_forecast(request):
    return null
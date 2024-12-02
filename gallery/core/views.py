from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.urls import reverse
from django.forms import modelformset_factory
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db import transaction

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
    artworks = Artwork.objects.all()
    recommended_artworks = artworks.order_by('?')[:2]
    context = {'artworks': artworks, 'recommended_artworks': recommended_artworks}
    
    return render(request, 'home.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def museum(request):
    galleries = Gallery.objects.all()
    return render(request, 'museum.html', {'galleries': galleries} )

def search(request):
    artworks = Artwork.objects.all()
    query = request.GET.get('query')
    results = artworks.filter(title=query) | artworks.filter(author=query)
    no_results_message = None

    if len(results) == 0:
        no_results_message = 'No matching artworks found.'

    print(results) 
    print(no_results_message)
    context = {'results': results, 'no_results_message': no_results_message}
    return render(request, 'search.html', context )


def gallery_view(request, gallery_name):
    '''
    display the info and all exhibited artworks of a gallery.
    '''
    gallery = Gallery.objects.get(gallery_name=gallery_name)
    #gallery_artworks = Artwork.objects.filter(gallery=gallery)
    gallery_artworks = Artwork.objects.filter(gallery=gallery).select_related('gallery')
    context = {
        'gallery': gallery,
        'artworks': gallery_artworks,
    }
    return render(request, 'gallery.html', context)

def register(request):
    """
    new account register
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


# Views for admin 

@login_required
def edit_gallery(request, gallery_name):
    """
    only staff allowed
    edit the info of the gallery. display all artworks exhibited in the gallery.
    """
    
    if not request.user.is_staff:
        messages.error(request, "Access Denied: Administrator privileges required. Please contact root for access.")
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
    only staff allowed
    change the properity value (except rating score) of an existing artwork.
    """

    if not request.user.is_staff:
        messages.error(request, "Access Denied: Administrator privileges required. Please contact root for access.")
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
    only staff allowed
    add a new artwork
    """

    if not request.user.is_staff:
        messages.error(request, "Access Denied: Administrator privileges required. Please contact root for access.")
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
    only staff allowed
    add a new author
    """

    if not request.user.is_staff:
        messages.error(request, "Access Denied: Administrator privileges required. Please contact root for access.")
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
    only staff allowed
    add a new styletag
    """
    if not request.user.is_staff:
        messages.error(request, "Access Denied: Administrator privileges required. Please contact root for access.")
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
    artwork = get_object_or_404(Artwork, title=artwork_title)
    context = {
        'artwork': artwork,
    }
    return render(request, 'artwork.html', context)

def styletag_detail(request, tag_name):
    '''
    display the artworks of a specific style
    '''
    style_tag = get_object_or_404(StyleTag, tag_name=tag_name)
    
    artworks = style_tag.artwork.all()

    return render(request, 'styletag_detail.html', {
        'style_tag': style_tag,
        'artworks': artworks,
    })

    
def author(request, author_name):
    '''
    author introduction page. display all artworks of the same author.
    '''
    try:
        author_found = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        return HttpResponse("Author not found", status=404)

    artworks = Artwork.objects.filter(author=author_found).select_related('author')
    context = {
        'author': author_found,
        'artworks': artworks,
    }
    return render(request, 'author.html', context)


@login_required
def create_reservation(request):
    '''
    for users to create new reservation
    '''
    current_reservations = None
    capacity = None

    if request.method == 'POST':
        form = ReservationOrderForm(request.POST)
        if form.is_valid():
            gallery = form.cleaned_data['gallery']
            order_date = form.cleaned_data['order_date']
            num_people = form.cleaned_data['num_people']

            with transaction.atomic():
                gallery = Gallery.objects.select_for_update().get(gallery_name=gallery.gallery_name)

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
    finished_paginator = Paginator(finished_reservations_list, 5)

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
    '''
    calculate the capacity and current_reservation of the selected date and gallery.
    '''
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

from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.urls import reverse
from django.forms import modelformset_factory
from django.db import IntegrityError

from .models import Gallery, Artwork, Author, StyleTag
from .forms import CustomUserCreationForm, GalleryForm, ArtworkForm, ArtworkFormSet, AuthorForm, StyleTagForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        register_form = CustomUserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            messages.success(request, 'Register Suceed!')
            return redirect('home')
    else:
        register_form = CustomUserCreationForm()
    return render(request, 'register.html', {'form':register_form})

@login_required
def different_view_example(request):
    if request.user.is_staff:
        return render(request, 'admin_page.html')
    else:
        return render(request, 'user_page.html')
    
def gallery_detail(request, gallery_name):
    formatted_gallery_name = gallery_name.replace('_', ' ').title()
    gallery = get_object_or_404(Gallery, gallery_name=formatted_gallery_name)
    return render(request, 'gallery_detail.html', {'gallery': gallery})


def edit_gallery(request, gallery_name):
    gallery = get_object_or_404(Gallery, gallery_name=gallery_name)
    
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=gallery)
        formset = ArtworkFormSet(request.POST, request.FILES, instance=gallery)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('edit_gallery', gallery_name=gallery.gallery_name)
    else:
        form = GalleryForm(instance=gallery)
        formset = ArtworkFormSet(instance=gallery)

    return render(request, 'edit_gallery.html', {
        'form': form, 
        'formset': formset,
        'gallery': gallery
    })

def edit_artwork_view(request, gallery_name, artwork_title):
    gallery = get_object_or_404(Gallery, gallery_name=gallery_name)
    artwork = get_object_or_404(Artwork, title=artwork_title, gallery=gallery)

    AuthorFormSet = modelformset_factory(Author, form=AuthorForm, extra=1, can_delete=True)
    if request.method == 'POST':
        artwork_form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        author_formset = AuthorFormSet(request.POST, queryset=Author.objects.filter(artwork=artwork))
        if artwork_form.is_valid() and author_formset.is_valid():
            artwork_form.save()
            author_formset.save()
            return redirect('edit_gallery', gallery_name=gallery.gallery_name)
    else:
        artwork_form = ArtworkForm(instance=artwork)
        author_formset = AuthorFormSet(queryset=Author.objects.filter(artwork=artwork))
    
    return render(request, 'edit_artwork.html', {
        'artwork_form': artwork_form,
        'author_formset': author_formset,
        'gallery': gallery,
        'artwork': artwork
    })


def add_artwork_view(request, gallery_name):
    gallery = get_object_or_404(Gallery, gallery_name=gallery_name)
    
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                print("222")
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

def add_author_view(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            previous_url = request.META.get('HTTP_REFERER')
            return redirect(previous_url) if previous_url else redirect('edit_gallery', gallery_name=request.GET.get('gallery_name'))
    else:
        form = AuthorForm()

    return render(request, 'add_author.html', {'form': form})

from .forms import StyleTagForm


def add_styletag_view(request):
    if request.method == 'POST':
        form = StyleTagForm(request.POST)
        if form.is_valid():
            form.save()
            previous_url = request.META.get('HTTP_REFERER')
            return redirect(previous_url) if previous_url else redirect('edit_gallery', gallery_name=request.GET.get('gallery_name'))
    else:
        form = StyleTagForm()

    return render(request, 'add_styletag.html', {'form': form})
        
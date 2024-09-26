from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import Gallery
from .forms import CustomUserCreationForm

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
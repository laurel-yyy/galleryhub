from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username','email', 'password1', 'password2')
    
    def clean_password2(self):
        return self.cleaned_data.get('password2')
    
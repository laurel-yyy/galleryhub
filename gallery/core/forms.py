from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Gallery, Artwork, Author, StyleTag

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username','email', 'password1', 'password2')
    
    def clean_password2(self):
        return self.cleaned_data.get('password2')
    

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image', 'description', 'visitor_capacity']
    
    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({
            'rows': 7,
            'cols': 100,
            'class': 'form-control',
            'style': 'white-space: pre-wrap;' 
        })
        self.fields['visitor_capacity'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control'
        })

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'description']


class StyleTagForm(forms.ModelForm):
    class Meta:
        model = StyleTag
        fields = ['tag_name', 'description']


class ArtworkForm(forms.ModelForm):
    styletags = forms.ModelMultipleChoiceField(
        queryset=StyleTag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


    class Meta:
        model = Artwork
        fields = ['title', 'author', 'description', 'image', 'year']

    
    def __init__(self, *args, **kwargs):
        super(ArtworkForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['styletags'].initial = self.instance.styletag.all()
    
    def save(self, commit=True):
        instance = super(ArtworkForm, self).save(commit=False)
        if commit:
            instance.save() 
            instance.styletag.clear()
            for tag in self.cleaned_data['styletags']:
                tag.artwork.add(instance)
        return instance
    
ArtworkFormSet = forms.inlineformset_factory( Gallery, Artwork, form=ArtworkForm, extra=1, can_delete=True)

from django import forms
from .models import Folder
from django.contrib.auth.models import User
import re


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class FolderForm(forms.ModelForm):
    
    class Meta:
        model = Folder
        fields = ['name', 'description', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'start_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'end_date':   forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }

class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': '[A-Za-z0-9.\-]+',
            'title': 'Solo letras, dígitos, puntos y guiones',
            'required': True,
        })
    )
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'required': True,
            'minlength': 8,
        }),
    )
    password2 = forms.CharField(
        label="Confirmación de contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'required': True,
            'minlength': 8,
        }),
    )

    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.fullmatch(r'[A-Za-z0-9.\-]+', username):
            raise forms.ValidationError("Usuario inválido: solo letras, dígitos, puntos y guiones.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', "Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        user = User(username=self.cleaned_data['username'])
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
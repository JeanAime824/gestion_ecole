from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Utilisateur

# Formulaire de connexion
class ConnexionForm(AuthenticationForm):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('responsable', 'Responsable'),
    ]
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(label="Type de compte", choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

# Formulaire de création de responsable (admin uniquement)
class ResponsableCreationForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'nom', 'prenom', 'sexe', 'contact', 'password1', 'password2']

    nom = forms.CharField(label="Nom", widget=forms.TextInput(attrs={'class': 'form-control'}))
    prenom = forms.CharField(label="Prénom", widget=forms.TextInput(attrs={'class': 'form-control'}))
    sexe = forms.ChoiceField(label="Sexe", choices=Utilisateur.SEXE, widget=forms.Select(attrs={'class': 'form-control'}))
    contact = forms.CharField(label="Contact", widget=forms.TextInput(attrs={'class': 'form-control'}))

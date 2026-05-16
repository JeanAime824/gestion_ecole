from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Utilisateur, Classe, Eleve, Paiement, Note

class ConnexionForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ResponsableCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Nom", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Prénom", widget=forms.TextInput(attrs={'class': 'form-control'}))
    sexe = forms.ChoiceField(label="Sexe", choices=Utilisateur.SEXE, widget=forms.Select(attrs={'class': 'form-control'}))
    contact = forms.CharField(label="Contact", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'sexe', 'contact', 'password1', 'password2']

class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ['nom', 'niveau']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'niveau': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EleveForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ['nom', 'prenom', 'date_naissance', 'classe']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
        }

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['eleve', 'montant', 'type_paiement', 'commentaire']
        widgets = {
            'eleve': forms.Select(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'type_paiement': forms.Select(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['eleve', 'matiere', 'valeur', 'date_evaluation']
        widgets = {
            'eleve': forms.Select(attrs={'class': 'form-control'}),
            'matiere': forms.TextInput(attrs={'class': 'form-control'}),
            'valeur': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 20}),
            'date_evaluation': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

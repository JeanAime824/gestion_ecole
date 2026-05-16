from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Avg, Count
from django.db.models.functions import TruncMonth
from .forms import (
    ConnexionForm, ResponsableCreationForm, ClasseForm,
    EleveForm, PaiementForm, NoteForm
)
from .models import Classe, Eleve, Utilisateur, Paiement, Note
import json

def is_admin(user):
    return user.role == 'administrateur' or user.is_superuser

def connexion_view(request):
    if request.method == "POST":
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if user.role == "administrateur" or user.is_superuser:
                    return redirect('admin_dashboard')
                elif user.role == "responsable":
                    return redirect('responsable_dashboard')
                else:
                    form.add_error(None, "Le rôle de cet utilisateur n'est pas défini.")
            else:
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = ConnexionForm()
    return render(request, 'login.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def ajouter_responsable(request):
    if request.method == "POST":
        form = ResponsableCreationForm(request.POST)
        if form.is_valid():
            responsable = form.save(commit=False)
            responsable.role = 'responsable'
            responsable.save()
            return redirect('admin_dashboard')
    else:
        form = ResponsableCreationForm()
    return render(request, 'ajouter_responsable.html', {'form': form})

@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        return redirect('responsable_dashboard')

    total_eleves = Eleve.objects.count()
    total_paiements = Paiement.objects.aggregate(Sum('montant'))['montant__sum'] or 0
    total_classes = Classe.objects.count()
    moyenne_generale = Note.objects.aggregate(Avg('valeur'))['valeur__avg'] or 0

    stats_classes = Classe.objects.annotate(nb_eleves=Count('eleves'))
    labels_classes = [c.nom for c in stats_classes]
    data_classes = [c.nb_eleves for c in stats_classes]

    paiements_mensuels = Paiement.objects.annotate(month=TruncMonth('date_paiement')) \
        .values('month').annotate(total=Sum('montant')).order_by('month')

    labels_revenus = [p['month'].strftime("%b %Y") for p in paiements_mensuels]
    data_revenus = [float(p['total']) for p in paiements_mensuels]

    context = {
        'total_eleves': total_eleves,
        'total_paiements': total_paiements,
        'total_classes': total_classes,
        'moyenne_generale': round(moyenne_generale, 2),
        'labels_classes': json.dumps(labels_classes),
        'data_classes': json.dumps(data_classes),
        'labels_revenus': json.dumps(labels_revenus),
        'data_revenus': json.dumps(data_revenus),
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def responsable_dashboard(request):
    if request.user.role != "responsable":
        return redirect('admin_dashboard')
    total_eleves = Eleve.objects.count()
    return render(request, 'responsable_dashboard.html', {'total_eleves': total_eleves})

def deconnexion_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

# --- GESTION DES CLASSES ---
@login_required
@user_passes_test(is_admin)
def liste_classes(request):
    classes = Classe.objects.all()
    return render(request, 'liste_classes.html', {'classes': classes})

@login_required
@user_passes_test(is_admin)
def ajouter_classe(request):
    if request.method == "POST":
        form = ClasseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_classes')
    else:
        form = ClasseForm()
    return render(request, 'ajouter_classe.html', {'form': form})

# --- GESTION DES ÉLÈVES ---
@login_required
def liste_eleves(request):
    eleves = Eleve.objects.all()
    return render(request, 'liste_eleves.html', {'eleves': eleves})

@login_required
def ajouter_eleve(request):
    if request.method == "POST":
        form = EleveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_eleves')
    else:
        form = EleveForm()
    return render(request, 'ajouter_eleve.html', {'form': form})

# --- GESTION DES PAIEMENTS ---
@login_required
def liste_paiements(request):
    paiements = Paiement.objects.all().order_by('-date_paiement')
    return render(request, 'liste_paiements.html', {'paiements': paiements})

@login_required
def ajouter_paiement(request):
    if request.method == "POST":
        form = PaiementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_paiements')
    else:
        form = PaiementForm()
    return render(request, 'ajouter_paiement.html', {'form': form})

# --- GESTION DES NOTES ---
@login_required
def liste_notes(request):
    notes = Note.objects.all().order_by('-date_evaluation')
    return render(request, 'liste_notes.html', {'notes': notes})

@login_required
def ajouter_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_notes')
    else:
        form = NoteForm()
    return render(request, 'ajouter_note.html', {'form': form})

# --- RAPPORTS ET STATISTIQUES ---
@login_required
@user_passes_test(is_admin)
def rapports_view(request):
    total_eleves = Eleve.objects.count()
    total_paiements = Paiement.objects.aggregate(Sum('montant'))['montant__sum'] or 0
    moyenne_generale = Note.objects.aggregate(Avg('valeur'))['valeur__avg'] or 0

    repartition_classe = Classe.objects.annotate(nb_eleves=Count('eleves'))
    derniers_paiements = Paiement.objects.all().order_by('-date_paiement')[:5]

    context = {
        'total_eleves': total_eleves,
        'total_paiements': total_paiements,
        'moyenne_generale': round(moyenne_generale, 2),
        'repartition_classe': repartition_classe,
        'derniers_paiements': derniers_paiements,
    }
    return render(request, 'rapports.html', context)

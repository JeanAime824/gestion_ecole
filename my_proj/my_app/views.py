from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Avg, Count
from .forms import ConnexionForm, ResponsableCreationForm
from .models import Classe, Eleve, Utilisateur, Paiement, Note

# Vérifie si l'utilisateur est admin
def is_admin(user):
    return user.role == 'administrateur'

# Vue de connexion avec redirection selon le rôle
def connexion_view(request):
    if request.method == "POST":
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']  # Récupération du choix

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Redirection basée sur le rôle réel en base
                if user.role == "administrateur" or user.is_superuser:
                    return redirect('admin_dashboard')
                elif user.role == "responsable":
                    return redirect('responsable_dashboard')
                else:
                    # Cas où le rôle n'est pas défini
                    form.add_error(None, "Le rôle de cet utilisateur n'est pas défini.")
            else:
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = ConnexionForm()

    return render(request, 'login.html', {'form': form})


# Vue pour ajouter un responsable (admin seulement)
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

# Dashboard admin
@login_required
#@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Dashboard responsable
@login_required
def responsable_dashboard(request):
    if request.user.role != "responsable":
        return redirect('login')
    return render(request, 'responsable_dashboard.html')

# Vue de déconnexion
def deconnexion_view(request):
    logout(request)
    return redirect('login')

# Vue de profil
@login_required
def profile_view(request):
    return render(request, 'profile.html')

# --- GESTION DES CLASSES (ADMIN) ---
@login_required
@user_passes_test(is_admin)
def liste_classes(request):
    classes = Classe.objects.all()
    return render(request, 'liste_classes.html', {'classes': classes})

@login_required
@user_passes_test(is_admin)
def ajouter_classe(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        niveau = request.POST.get('niveau')
        Classe.objects.create(nom=nom, niveau=niveau)
        return redirect('liste_classes')
    return render(request, 'ajouter_classe.html')

# --- GESTION DES ÉLÈVES (RESPONSABLE & ADMIN) ---
@login_required
def liste_eleves(request):
    eleves = Eleve.objects.all()
    return render(request, 'liste_eleves.html', {'eleves': eleves})

@login_required
def ajouter_eleve(request):
    classes = Classe.objects.all()
    if request.method == "POST":
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        date_naissance = request.POST.get('date_naissance')
        classe_id = request.POST.get('classe')
        classe = get_object_or_404(Classe, id=classe_id)
        Eleve.objects.create(nom=nom, prenom=prenom, date_naissance=date_naissance, classe=classe)
        return redirect('liste_eleves')
    return render(request, 'ajouter_eleve.html', {'classes': classes})

# --- GESTION DES PAIEMENTS (ECOLAGE) ---
@login_required
def liste_paiements(request):
    paiements = Paiement.objects.all().order_by('-date_paiement')
    return render(request, 'liste_paiements.html', {'paiements': paiements})

@login_required
def ajouter_paiement(request):
    eleves = Eleve.objects.all()
    if request.method == "POST":
        eleve_id = request.POST.get('eleve')
        montant = request.POST.get('montant')
        type_p = request.POST.get('type_paiement')
        commentaire = request.POST.get('commentaire')

        eleve = get_object_or_404(Eleve, id=eleve_id)
        Paiement.objects.create(
            eleve=eleve,
            montant=montant,
            type_paiement=type_p,
            commentaire=commentaire
        )
        return redirect('liste_paiements')

    types = Paiement.TYPES
    return render(request, 'ajouter_paiement.html', {'eleves': eleves, 'types': types})

# --- GESTION DES NOTES ---
@login_required
def liste_notes(request):
    notes = Note.objects.all().order_by('-date_evaluation')
    return render(request, 'liste_notes.html', {'notes': notes})

@login_required
def ajouter_note(request):
    eleves = Eleve.objects.all()
    if request.method == "POST":
        eleve_id = request.POST.get('eleve')
        matiere = request.POST.get('matiere')
        valeur = request.POST.get('valeur')
        date_e = request.POST.get('date_evaluation')

        eleve = get_object_or_404(Eleve, id=eleve_id)
        Note.objects.create(
            eleve=eleve,
            matiere=matiere,
            valeur=valeur,
            date_evaluation=date_e
        )
        return redirect('liste_notes')
    return render(request, 'ajouter_note.html', {'eleves': eleves})

# --- RAPPORTS ET STATISTIQUES (ADMIN) ---
@login_required
@user_passes_test(is_admin)
def rapports_view(request):
    total_eleves = Eleve.objects.count()
    total_paiements = Paiement.objects.aggregate(Sum('montant'))['montant__sum'] or 0
    moyenne_generale = Note.objects.aggregate(Avg('valeur'))['valeur__avg'] or 0

    # Répartition par classe
    repartition_classe = Classe.objects.annotate(nb_eleves=Count('eleves'))

    # Derniers paiements
    derniers_paiements = Paiement.objects.all().order_by('-date_paiement')[:5]

    context = {
        'total_eleves': total_eleves,
        'total_paiements': total_paiements,
        'moyenne_generale': round(moyenne_generale, 2),
        'repartition_classe': repartition_classe,
        'derniers_paiements': derniers_paiements,
    }
    return render(request, 'rapports.html', context)

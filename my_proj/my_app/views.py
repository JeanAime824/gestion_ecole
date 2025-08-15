from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ConnexionForm, ResponsableCreationForm

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

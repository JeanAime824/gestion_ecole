from django.urls import path
from .views import (
    connexion_view, ajouter_responsable, admin_dashboard,
    responsable_dashboard, deconnexion_view, profile_view,
    liste_classes, ajouter_classe, liste_eleves, ajouter_eleve,
    liste_paiements, ajouter_paiement, liste_notes, ajouter_note,
    rapports_view
)

urlpatterns = [
    path('', connexion_view, name='login'),
    path('logout/', deconnexion_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('ajouter-responsable/', ajouter_responsable, name='ajouter_responsable'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('responsable-dashboard/', responsable_dashboard, name='responsable_dashboard'),
    path('rapports/', rapports_view, name='rapports'),

    # Classes
    path('classes/', liste_classes, name='liste_classes'),
    path('classes/ajouter/', ajouter_classe, name='ajouter_classe'),

    # Eleves
    path('eleves/', liste_eleves, name='liste_eleves'),
    path('eleves/ajouter/', ajouter_eleve, name='ajouter_eleve'),

    # Paiements
    path('paiements/', liste_paiements, name='liste_paiements'),
    path('paiements/ajouter/', ajouter_paiement, name='ajouter_paiement'),

    # Notes
    path('notes/', liste_notes, name='liste_notes'),
    path('notes/ajouter/', ajouter_note, name='ajouter_note'),
]

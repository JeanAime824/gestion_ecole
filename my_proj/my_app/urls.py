from django.urls import path
from .views import (
    connexion_view, ajouter_responsable, admin_dashboard,
    responsable_dashboard, deconnexion_view, profile_view,
    liste_classes, ajouter_classe, liste_eleves, ajouter_eleve
)

urlpatterns = [
    path('', connexion_view, name='login'),
    path('logout/', deconnexion_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('ajouter-responsable/', ajouter_responsable, name='ajouter_responsable'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('responsable-dashboard/', responsable_dashboard, name='responsable_dashboard'),

    # Classes
    path('classes/', liste_classes, name='liste_classes'),
    path('classes/ajouter/', ajouter_classe, name='ajouter_classe'),

    # Eleves
    path('eleves/', liste_eleves, name='liste_eleves'),
    path('eleves/ajouter/', ajouter_eleve, name='ajouter_eleve'),
]

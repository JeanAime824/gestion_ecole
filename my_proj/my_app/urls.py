from django.urls import path
from .views import (
    connexion_view, ajouter_responsable, admin_dashboard,
    responsable_dashboard, deconnexion_view, profile_view,
    liste_classes, ajouter_classe, liste_eleves, ajouter_eleve, liste_responsables,
    liste_paiements, ajouter_paiement, liste_notes, ajouter_note,
    rapports_view, export_eleves_csv, export_eleves_xlsx,
    export_responsables_csv, export_responsables_xlsx, export_paiements_csv, export_paiements_xlsx,
    export_notes_csv, export_notes_xlsx, export_rapports_xlsx, export_eleve_detail_csv, export_eleve_detail_xlsx,
    export_responsable_detail_csv, export_responsable_detail_xlsx
)

urlpatterns = [
    path('', connexion_view, name='login'),
    path('logout/', deconnexion_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('ajouter-responsable/', ajouter_responsable, name='ajouter_responsable'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('responsable-dashboard/', responsable_dashboard, name='responsable_dashboard'),
    path('rapports/', rapports_view, name='rapports'),
    path('rapports/export/xlsx/', export_rapports_xlsx, name='export_rapports_xlsx'),

    # Classes
    path('classes/', liste_classes, name='liste_classes'),
    path('classes/ajouter/', ajouter_classe, name='ajouter_classe'),

    # Eleves
    path('eleves/', liste_eleves, name='liste_eleves'),
    path('eleves/ajouter/', ajouter_eleve, name='ajouter_eleve'),
    path('responsables/', liste_responsables, name='liste_responsables'),
    path('eleves/export/csv/', export_eleves_csv, name='export_eleves_csv'),
    path('eleves/export/xlsx/', export_eleves_xlsx, name='export_eleves_xlsx'),
    path('eleves/export/<int:eleve_id>/', export_eleve_detail_csv, name='export_eleve_detail_csv'),
    path('eleves/export/<int:eleve_id>/xlsx/', export_eleve_detail_xlsx, name='export_eleve_detail_xlsx'),
    path('responsables/export/csv/', export_responsables_csv, name='export_responsables_csv'),
    path('responsables/export/xlsx/', export_responsables_xlsx, name='export_responsables_xlsx'),
    path('responsables/export/<int:user_id>/', export_responsable_detail_csv, name='export_responsable_detail_csv'),
    path('responsables/export/<int:user_id>/xlsx/', export_responsable_detail_xlsx, name='export_responsable_detail_xlsx'),
    path('paiements/export/csv/', export_paiements_csv, name='export_paiements_csv'),
    path('paiements/export/xlsx/', export_paiements_xlsx, name='export_paiements_xlsx'),
    path('notes/export/csv/', export_notes_csv, name='export_notes_csv'),
    path('notes/export/xlsx/', export_notes_xlsx, name='export_notes_xlsx'),

    # Paiements
    path('paiements/', liste_paiements, name='liste_paiements'),
    path('paiements/ajouter/', ajouter_paiement, name='ajouter_paiement'),

    # Notes
    path('notes/', liste_notes, name='liste_notes'),
    path('notes/ajouter/', ajouter_note, name='ajouter_note'),
]

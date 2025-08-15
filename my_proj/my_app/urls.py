from django.urls import path
from .views import connexion_view, ajouter_responsable, admin_dashboard, responsable_dashboard

urlpatterns = [
    path('', connexion_view, name='login'),
    path('ajouter-responsable/', ajouter_responsable, name='ajouter_responsable'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('responsable-dashboard/', responsable_dashboard, name='responsable_dashboard'),
]

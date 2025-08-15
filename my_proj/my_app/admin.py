from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    # Les champs à afficher dans la liste
    list_display = ('username', 'email', 'role', 'sexe', 'contact', 'is_staff')

    # Les champs à utiliser dans le formulaire d'édition
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('role', 'sexe', 'contact')}),
    )

    # Les champs à utiliser dans le formulaire de création
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {'fields': ('role', 'sexe', 'contact')}),
    )

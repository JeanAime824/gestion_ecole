from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UtilisateurManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('Le nom d’utilisateur est obligatoire')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'administrateur')  # valeur par défaut

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class Utilisateur(AbstractUser):
    ROLES = [
        ('administrateur', 'Administrateur'),
        ('responsable', 'Responsable'),
    ]
    SEXE = [
        ('homme', 'Homme'),
        ('femme', 'Femme'),
    ]
    role = models.CharField(max_length=20, choices=ROLES, blank=True, null=True)
    sexe = models.CharField(max_length=20, choices=SEXE, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)

    objects = UtilisateurManager()

    def __str__(self):
        return f"{self.username} ({self.role})"

class Classe(models.Model):
    nom = models.CharField(max_length=50)
    niveau = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nom} ({self.niveau})"

class Eleve(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='eleves')

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Paiement(models.Model):
    TYPES = [
        ('frais_inscription', 'Frais d\'inscription'),
        ('ecolage', 'Écolage'),
        ('autre', 'Autre'),
    ]
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='paiements')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField(auto_now_add=True)
    type_paiement = models.CharField(max_length=20, choices=TYPES)
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.eleve} - {self.montant} ({self.type_paiement})"

class Note(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='notes')
    matiere = models.CharField(max_length=100)
    valeur = models.DecimalField(max_digits=5, decimal_places=2)
    date_evaluation = models.DateField()

    def __str__(self):
        return f"{self.eleve} - {self.matiere}: {self.valeur}"

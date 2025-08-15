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

from django.test import TestCase
from django.urls import reverse
from .models import Utilisateur, Classe, Eleve, Paiement, Note

class SchoolManagementTests(TestCase):
    def setUp(self):
        self.admin = Utilisateur.objects.create_user(username='admin', password='password123', role='administrateur')
        self.responsable = Utilisateur.objects.create_user(username='resp', password='password123', role='responsable')
        self.classe = Classe.objects.create(nom='6eme A', niveau='6eme')
        self.eleve = Eleve.objects.create(nom='Doe', prenom='John', date_naissance='2010-01-01', classe=self.classe)

    def test_rapports_view_access(self):
        self.client.login(username='admin', password='password123')
        response = self.client.get(reverse('rapports'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rapports et Statistiques')

    def test_ajouter_paiement(self):
        self.client.login(username='admin', password='password123')
        response = self.client.post(reverse('ajouter_paiement'), {
            'eleve': self.eleve.id,
            'montant': 50000,
            'type_paiement': 'ecolage',
            'commentaire': 'Janvier'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Paiement.objects.count(), 1)

    def test_ajouter_note(self):
        self.client.login(username='resp', password='password123')
        response = self.client.post(reverse('ajouter_note'), {
            'eleve': self.eleve.id,
            'matiere': 'Maths',
            'valeur': 15,
            'date_evaluation': '2023-10-01'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Note.objects.count(), 1)

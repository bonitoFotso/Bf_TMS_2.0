from django.db.models import F, ExpressionWrapper, fields
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save, pre_delete
from django.db.utils import IntegrityError

from django.dispatch import receiver
from apps.clients.models import *
from apps.ressource.models import *
from datetime import date
from datetime import timedelta
from django.utils import timezone
from django.utils.text import slugify
#importation des signaux personaliser


# Créez un signal personnalisé
class TechnicienTacheManager(models.Manager):
    def add_technicien(self, tache, technicien, date_debut=None, date_fin=None, ok=False):
        """
        Ajoute un technicien à une tâche avec les informations spécifiées.
        """
        technicien_tache = self.create(tache=tache, technicien=technicien, date_debut=date_debut, date_fin=date_fin, ok=ok)
        return technicien_tache

    def remove_technicien(self, tache, technicien):
        """
        Supprime un technicien associé à une tâche.
        """
        self.filter(tache=tache, technicien=technicien).delete()

    def get_techniciens(self, tache):
        """
        Récupère la liste des techniciens associés à une tâche.
        """
        return self.filter(tache=tache)
    
    def get_technicien_tache(self, tache, technicien):
        """
        Récupère l'objet TechnicienTache associé à une tâche et un technicien spécifiques.
        """
        return self.filter(tache=tache, technicien=technicien).first()

    def get_technicien_taches_technicien(self, technicien):
        """
        Récupère toutes les tâches associées à un technicien spécifique.
        """
        return self.filter(technicien=technicien)

    def get_technicien_taches_date(self, technicien, date):
        """
        Récupère toutes les tâches associées à un technicien à une date spécifique.
        """
        return self.filter(technicien=technicien, date_debut__lte=date, date_fin__gte=date)

    def annotate_duree(self):
        return self.annotate(
            duree=ExpressionWrapper(
                F('tache__date_fin') - F('tache__date_debut'),
                output_field=fields.DurationField()
            )
        )

class DonneeJour(models.Model):
    date = models.DateField()



jours = [
    ('lundi', 'lundi'),
    ('mardi', 'mardi'),
    ('mercredi', 'mercredi'),
    ('jeudi', 'jeudi'),
    ('vendredi', 'vendredi'),
    ('samedi', 'samedi'),
]

class Categorie(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now=True)  # Date de création automatique
    updatedAt = models.DateTimeField(auto_now_add=True)  # Date de mise à jour automatique
    def __str__(self):
        return self.nom

class Activite(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now=True)  # Date de création automatique
    updatedAt = models.DateTimeField(auto_now_add=True)  # Date de mise à jour automatique
    def __str__(self):
        return f"Activité de {self.nom}"
    

class Tache(models.Model):
    # Choix pour le champ 'status'
    STATUS_CHOICES = [
        ('En attente', 'En attente'),
        ('En cours', 'En cours'),
        ('En arrêt', 'En arrêt'),
        ('Effectué', 'Effectué'),

    ]
    PRIORITE_CHOICES = [
    ('Bas', 'Bas'),
    ('Moyen', 'Moyen'),
    ('Élevé', 'Élevé'),
]
    activite = models.ManyToManyField(Activite, verbose_name=_("Activite"), db_index=True)
    categorie = models.ManyToManyField(Categorie, verbose_name=_("Categorie"), db_index=True)
    nom = models.CharField(_("intitule"), max_length=200,db_index=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="En attente")  # Choix de statut
    appelant = models.ForeignKey(Appelant, verbose_name=_("Celui qui appelle"), on_delete=models.CASCADE)
    priorite = models.CharField(choices=PRIORITE_CHOICES, max_length=20)  # Choix de priorité
    description = models.CharField(max_length=500, null=False, default='description')
    n_OS = models.CharField(_("Numéro d'OS"), max_length=50, null=True, blank=True)
    ok = models.BooleanField(default=False)  # Champ pour indiquer si la tâche est terminée
    date_debut = models.DateTimeField(_("Date de début"), blank=True, null=True, )
    date_fin     = models.DateTimeField(_("Date de fin"), blank=True, null=True, )
    createdAt = models.DateTimeField(auto_now_add=True,db_index=True)  # Date de création automatique
    updatedAt = models.DateTimeField(auto_now=True,db_index=True)  # Date de mise à jour automatique
    assignations = models.ManyToManyField(Technicien, through='TechnicienTache',through_fields=('tache', 'technicien'))

    objects = models.Manager()  # Le gestionnaire par défaut
    technicien_tache_objects = TechnicienTacheManager() 
    def save(self, *args, **kwargs):
        # Si la tâche est nouvellement créée et n'a pas encore de date de début, la mettre en "En attente"
        if not self.id and not self.date_debut:
            self.status = 'En attente'
        # Si la tâche a une date de début, la mettre en "En cours"
        elif self.date_debut:
            self.status = 'En cours'
        # Si la tâche a un numéro d'OS, la mettre en "En facturation"
        if self.n_OS and self.ok:
            self.status = 'Effectué'

        super(Tache, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.nom  # Renvoie le nom unique de la tâche comme représentation en chaîne
    
    @property
    def is_active(self):
        return not self.status or (self.status != 'En arrêt' and timezone.now().date() <= self.date_fin)

    
    def get_progression(self):
        if self.is_active():
            total_days = (self.date_fin - self.date_debut).days
            elapsed_days = (timezone.now().date() - self.date_debut).days
            return min(100, (elapsed_days / total_days) * 100)
        else:
            return 0

    @property
    def is_overdue(self):
        return (
            self.status == 'En cours'
            and self.date_fin is not None
            and timezone.now() > self.date_fin
        )


    class Meta:
        verbose_name = _("Tache")
        verbose_name_plural = _("Taches")
        ordering = ['createdAt']

class TechnicienTache(models.Model):
    technicien = models.ForeignKey(Technicien, verbose_name=_("techniciens"), on_delete=models.CASCADE, blank=True, null=True)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    ok = models.BooleanField(_("tache effectuer"), default=False)
    date_debut = models.DateTimeField(_("Date de début"), null=True, blank=True)
    date_fin = models.DateTimeField(_("Date de fin"), null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)  # Date de création automatique

    class Meta:
        unique_together = (('technicien', 'tache'),)

    def save(self, *args, **kwargs):
        # Si la tâche n'a pas de date de début, mettre la date actuelle
        if not self.tache.date_debut:
            self.tache.date_debut = timezone.now()

        # Si la tâche n'a pas de date de fin, utiliser la date de fin du TechnicienTache
        if not self.tache.date_fin and self.date_fin:
            self.tache.date_fin = self.date_fin

        # Appeler la méthode save() du modèle parent pour effectuer la sauvegarde
        super(TechnicienTache, self).save(*args, **kwargs)

        # Mettre à jour la date de fin de la tâche si nécessaire
        if self.tache.date_fin and self.tache.date_fin > self.tache.date_debut:
            self.tache.save()

    def __str__(self):
        try:
            return self.technicien.nom
        except (Technicien.DoesNotExist, Tache.DoesNotExist):
            return 'TechnicienTache ID: %s' % self.id



    @property
    def get_duree(self):
        if self.tache.date_debut and self.tache.date_fin:
            if isinstance(self.tache.date_debut, datetime) and isinstance(self.tache.date_fin, datetime):
                duree = self.tache.date_fin - self.tache.date_debut
                days, seconds = duree.days, duree.seconds
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                return {
                    'days': days,
                    'hours': hours,
                    'minutes': minutes,
                }
        return {
            'days': 0,
            'hours': 0,
            'minutes': 0,
        }
        


class Rapport(models.Model):
    tache = models.ForeignKey(Tache, verbose_name=_("Tâche effectuée par le technicien"), on_delete=models.CASCADE)
    rapport_text = models.TextField(_("Rapport"))
    date_creation = models.DateTimeField(auto_now_add=True)
    technicien_list = models.CharField(_("liste des technicien"), max_length=250,null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rapport pour {self.technicien_tache.tache.nom} - {self.technicien_tache.technicien.nom}"

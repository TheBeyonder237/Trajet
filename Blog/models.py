from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


from django.db import models
from django.contrib.auth.models import User


class Ville(models.Model):
    """
    Représente une ville desservie par le réseau de transport interurbain.
    """
    nom = models.CharField(max_length=255, verbose_name="Nom de la ville")
    code_postal = models.CharField(max_length=10, verbose_name="Code postal")

    def __str__(self):
        return self.nom


class Station(models.Model):
    """
    Représente une station ou un arrêt au sein d'une ville.
    """
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, verbose_name="Ville associée")
    nom = models.CharField(max_length=255, verbose_name="Nom de la station")
    adresse = models.TextField(verbose_name="Adresse de la station")
    latitude = models.FloatField(verbose_name="Latitude géographique")
    longitude = models.FloatField(verbose_name="Longitude géographique")

    def __str__(self):
        return f"{self.nom} ({self.ville.nom})"


class CompagnieDeTransport(models.Model):
    """
    Représente une entreprise ou entité qui fournit des services de transport.
    """
    nom = models.CharField(max_length=255, verbose_name="Nom de la compagnie")
    description = models.TextField(blank=True, null=True, verbose_name="Description de la compagnie")

    def __str__(self):
        return self.nom


class Ligne(models.Model):
    """
    Représente une ligne de transport interurbain, e.g., une ligne de bus entre deux villes.
    """
    nom = models.CharField(max_length=255, verbose_name="Nom de la ligne", primary_key=True)
    compagnie = models.ForeignKey(CompagnieDeTransport, on_delete=models.CASCADE, verbose_name="Compagnie associée")
    depart = models.ForeignKey(Station, related_name="lignes_de_depart", on_delete=models.CASCADE,
                               verbose_name="Station de départ")
    arrivee = models.ForeignKey(Station, related_name="lignes_d_arrivee", on_delete=models.CASCADE,
                                verbose_name="Station d'arrivée")

    def __str__(self):
        return f"{self.depart} → {self.arrivee}"


class Horaires(models.Model):
    """
    Représente les horaires de départ et d'arrivée pour une ligne donnée.
    """
    ligne = models.ForeignKey(Ligne, on_delete=models.CASCADE, verbose_name="Ligne associée")
    heure_depart = models.TimeField(verbose_name="Heure de départ")
    heure_arrivee = models.TimeField(verbose_name="Heure d'arrivée")

    def __str__(self):
        return f"{self.ligne.nom} - {self.heure_depart} → {self.heure_arrivee}"


class Ticket(models.Model):
    """
    Gère les billets réservés par les utilisateurs pour une ligne à un horaire précis.
    """
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    ligne = models.ForeignKey(Ligne, on_delete=models.CASCADE, verbose_name="Ligne réservée")
    horaire = models.ForeignKey(Horaires, on_delete=models.CASCADE, verbose_name="Horaire réservé")
    date_reservation = models.DateField(verbose_name="Date de réservation")
    prix = models.FloatField(verbose_name="Prix du billet")

    def __str__(self):
        return f"Ticket de {self.utilisateur.username} pour {self.ligne.nom} à {self.horaire.heure_depart}"


class Vehicule(models.Model):
    """
    Représente les différents véhicules utilisés dans le transport, par exemple bus ou tramway.
    """
    TYPE_CHOICES = (
        ('bus', 'Bus'),
        ('tram', 'Tramway'),
        # Ajoutez d'autres types si nécessaire.
    )
    type_vehicule = models.CharField(max_length=255, choices=TYPE_CHOICES, verbose_name="Type de véhicule")
    lignes = models.ManyToManyField(Ligne, verbose_name="Lignes desservies")
    capacite = models.IntegerField(verbose_name="Capacité en passagers")

    def __str__(self):
        return f"{self.get_type_vehicule_display()} - Capacité: {self.capacite}"


class Categorie(models.Model):
    """
    Catégorie dans laquelle une vidéo peut être classée.
    """
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom


class Commentaire(models.Model):
    """
    Commentaires associés à une vidéo.
    """
    poste = models.ForeignKey('Poste', on_delete=models.CASCADE, related_name='commentaires')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    texte = models.TextField()
    date_publiee = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.username}: {self.texte[:50]}..."


class Poste(models.Model):
    """
    Vidéo stockée sur un service cloud et présentée sur la plateforme.
    """

    STATUT_CHOICES = (
        ('publique', 'Publique'),
        ('privee', 'Privée'),
        ('archivee', 'Archivée'),
    )

    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_publiee = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    url_video = models.URLField()
    url_thumbnail = models.URLField(blank=True, null=True)
    duree = models.DurationField(blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, blank=True, null=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='publique')
    note_moyenne = models.FloatField(default=0)
    nombre_votes = models.PositiveIntegerField(default=0)
    ligne = models.ForeignKey(Ligne, on_delete=models.CASCADE, verbose_name="Ligne associée")
    url_video = models.URLField(blank=True, null=True, verbose_name="Lien vidéo")
    video_upload = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name="Upload vidéo")

    def clean(self):
        if self.url_video and self.video_upload:
            raise ValidationError("Vous ne pouvez pas avoir à la fois une URL vidéo et une vidéo uploadée.")
        if not self.url_video and not self.video_upload:
            raise ValidationError("Veuillez fournir une URL vidéo ou uploader une vidéo.")

    def __str__(self):
        return self.titre

    def ajouter_note(self, note):
        """
        Ajoute une note à la vidéo et met à jour la note moyenne.
        """
        total_notes = self.note_moyenne * self.nombre_votes
        total_notes += note
        self.nombre_votes += 1
        self.note_moyenne = total_notes / self.nombre_votes
        self.save()

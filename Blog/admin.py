from django.contrib import admin
from django.utils.html import format_html

from .models import Poste, Categorie, Commentaire, Ville, Station, CompagnieDeTransport, Ligne, Horaires, Vehicule


# Pour Poste
class PosteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_publiee', 'categorie', 'statut')
    search_fields = ('titre', 'description')
    list_filter = ('statut', 'categorie', 'date_publiee')
    ordering = ['-date_publiee']
    date_hierarchy = 'date_publiee'
    readonly_fields = ["video_display"]

    def video_display(self, obj):
        if obj.video_upload:
            return format_html(
                '<video width="320" height="240" controls>'
                '  <source src="{}" type="video/mp4">'
                '  Votre navigateur ne supporte pas la vidéo.'
                '</video>',
                obj.video_upload.url
            )
        elif obj.url_video:
            return format_html(
                '<video width="320" height="240" controls>'
                '  <source src="{}" type="video/mp4">'
                '  Votre navigateur ne supporte pas la vidéo.'
                '</video>',
                obj.url_video
            )
        else:
            return "Aucune vidéo"

    video_display.short_description = 'Aperçu de la vidéo'


# Pour Categorie
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)


# Pour Commentaire
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('poste', 'utilisateur', 'date_publiee')
    search_fields = ('texte',)
    list_filter = ('date_publiee',)
    date_hierarchy = 'date_publiee'


# Pour Ville
class VilleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code_postal')
    search_fields = ('nom',)


# Pour Station
class StationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'adresse')
    search_fields = ('nom', 'adresse')


# Pour CompagnieDeTransport
class CompagnieAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom', 'description')


# Pour Ligne
class LigneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'compagnie', 'depart', 'arrivee')
    search_fields = ('nom',)


# Pour Horaires
class HorairesAdmin(admin.ModelAdmin):
    list_display = ('ligne', 'heure_depart', 'heure_arrivee')
    list_filter = ('ligne',)


# Pour Vehicule
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('type_vehicule', 'capacite')
    search_fields = ('type_vehicule',)


# Enregistrement des modèles avec leurs classes d'admin respectives
admin.site.register(Poste, PosteAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Commentaire, CommentaireAdmin)
admin.site.register(Ville, VilleAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(CompagnieDeTransport, CompagnieAdmin)
admin.site.register(Ligne, LigneAdmin)
admin.site.register(Horaires, HorairesAdmin)
admin.site.register(Vehicule, VehiculeAdmin)

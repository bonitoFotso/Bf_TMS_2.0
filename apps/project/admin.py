from django.contrib import admin
from .models import *


# Administration pour le modèle Categorie
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'createdAt', 'updatedAt')
    list_filter = ('createdAt', 'updatedAt')
    search_fields = ('nom', 'description')
    list_per_page = 10

# Administration pour le modèle Activite
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'createdAt', 'updatedAt')
    list_filter = ('createdAt', 'updatedAt')
    search_fields = ('nom', 'description', 'projet__nom')
    list_per_page = 10

admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Activite, ActiviteAdmin)

class TechnicienTacheInline(admin.TabularInline):
    model = TechnicienTache

class TacheAdmin(admin.ModelAdmin):
    #form = TacheForm
    list_display = ('nom', 'status', 'priorite', 'date_debut', 'date_fin', 'is_overdue')
    list_filter = ('status', 'priorite', 'date_debut', 'date_fin')
    search_fields = ('nom', 'description', 'n_OS')
    inlines = [TechnicienTacheInline]
    date_hierarchy = 'date_debut'
    actions = ['marquer_effectue']

    def marquer_effectue(self, request, queryset):
        queryset.update(status='Effectué')
    marquer_effectue.short_description = "Marquer les tâches sélectionnées comme effectuées"

admin.site.register(Tache, TacheAdmin)

@admin.register(TechnicienTache)
class TechnicienTacheAdmin(admin.ModelAdmin):
    list_display = ('technicien', 'tache', 'ok', 'date_debut', 'date_fin')
    list_filter = ('technicien', 'tache', 'ok')
    search_fields = ('technicien__nom', 'tache__nom')
    date_hierarchy = 'date_debut'
    ordering = ('-date_debut',)
    

@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    list_display = ('tache', 'date_creation')
    list_filter = ('date_creation',)
    search_fields = ('tache__nom', 'rapport_text')
    date_hierarchy = 'date_creation'
    ordering = ('-date_creation',)




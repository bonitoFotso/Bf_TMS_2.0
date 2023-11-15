from rest_framework import generics, status
from rest_framework.response import Response
from apps.project.models import Tache, Activite, Categorie, TechnicienTache
from .serializers import (TacheSerializer, AgenceSerializer, TechnicienSerializer, ClientSerializer, AppelantSerializer, ActiviteSerializer, CategorieSerializer, TSerializer)
from apps.clients.models import Agence, Client, Appelant
from apps.ressource.models import Technicien
from rest_framework import serializers

class AllView(generics.ListAPIView):
    serializer_class_agence = AgenceSerializer
    serializer_class_client = ClientSerializer
    serializer_class_appelant = AppelantSerializer
    serializer_class_technicien = TechnicienSerializer
    serializer_class_activite = ActiviteSerializer
    serializer_class_categorie = CategorieSerializer

    def get_queryset_agence(self):
        return Agence.objects.all()

    def get_queryset_client(self):
        return Client.objects.all()

    def get_queryset_appelant(self):
        return Appelant.objects.all()

    def get_queryset_technicien(self):
        return Technicien.objects.all()
    
    def get_queryset_activite(self):
        return Activite.objects.all()

    def get_queryset_categorie(self):
        return Categorie.objects.all()

    def list(self, request, *args, **kwargs):
        agences = self.get_queryset_agence()
        clients = self.get_queryset_client()
        appelants = self.get_queryset_appelant()
        techniciens = self.get_queryset_technicien()
        activites = self.get_queryset_activite()
        categories = self.get_queryset_categorie()

        serializer_agence = self.serializer_class_agence(agences, many=True)
        serializer_client = self.serializer_class_client(clients, many=True)
        serializer_appelant = self.serializer_class_appelant(appelants, many=True)
        serializer_technicien = self.serializer_class_technicien(techniciens, many=True)
        serializer_activite = self.serializer_class_activite(activites, many=True)
        serializer_categorie = self.serializer_class_categorie(categories, many=True)

        response_data = {
            'agences': serializer_agence.data,
            'clients': serializer_client.data,
            'appelants': serializer_appelant.data,
            'techniciens': serializer_technicien.data,
            'activites': serializer_activite.data,
            'categories': serializer_categorie.data
        }

        return Response(response_data)



class TacheListCreateView(generics.ListCreateAPIView):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer
    #filter_backends = [filters.DateFromToRangeFilter, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'status', 'appelant__name', 'agence__name', 'agence__siege__name', 'agence__siege__n_client']
    ordering_fields = ['date_debut', 'date_fin', 'createdAt', 'updatedAt']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    


class TacheDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tache.objects.all()
    serializer_class = TSerializer

    def perform_update(self, serializer):
        # Appelez d'abord la méthode perform_update du parent pour mettre à jour la tâche elle-même
        instance = serializer.save()

        # Ensuite, mettez à jour les techniciens associés à la tâche
        techniciens_data = self.request.data.get('assignations', [])  # Supposons que les techniciens soient envoyés sous la clé 'assignations'
        TechnicienTache.objects.filter(tache=instance).delete()  # Supprimez toutes les relations existantes

        for technicien_id in techniciens_data:
            TechnicienTache.objects.create(tache=instance, technicien_id=technicien_id)


class TacheCreateView(generics.CreateAPIView):
    queryset = Tache.objects.all()
    serializer_class = TSerializer
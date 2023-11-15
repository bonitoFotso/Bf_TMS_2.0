from rest_framework import generics
from apps.project.models import Tache,Categorie, Activite
from apps.clients.models import  Appelant,Client,Agence
from .serializers import (TacheSerializer,CategorieSerializer, 
                          ActiviteSerializer, AppelantSerializer,
                          ClientSerializer,AgenceSerializer,
                          TechnicienSerializer)
from apps.ressource.models import Technicien
from rest_framework.permissions import IsAuthenticated
from account.models import User
from .serializers import UserSerializer
from rest_framework import filters



#class TechnicienTacheListCreateView(generics.ListCreateAPIView):
#    queryset = TechnicienTache.objects.all()
#    serializer_class = TechnicienTacheSerializer
#    
#class RapportListCreateView(generics.ListCreateAPIView):
#    queryset = Rapport.objects.all()
#    serializer_class = RapportSerializer
    

class CategorieListCreateView(generics.ListCreateAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class CategorieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class ActiviteListCreateView(generics.ListCreateAPIView):
    queryset = Activite.objects.all()
    serializer_class = ActiviteSerializer

class ActiviteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activite.objects.all()
    serializer_class = ActiviteSerializer

class AppelantListCreateView(generics.ListCreateAPIView):
    queryset = Appelant.objects.all()
    serializer_class = AppelantSerializer

class AppelantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appelant.objects.all()
    serializer_class = AppelantSerializer

class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]



class AgenceListCreateView(generics.ListCreateAPIView):
    queryset = Agence.objects.all()
    serializer_class = AgenceSerializer

class AgenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agence.objects.all()
    serializer_class = AgenceSerializer

# Liste et création de techniciens
class TechnicienListCreateView(generics.ListCreateAPIView):
    queryset = Technicien.objects.all()
    serializer_class = TechnicienSerializer

# Récupération, mise à jour et suppression d'un technicien par ID
class TechnicienDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Technicien.objects.all()
    serializer_class = TechnicienSerializer
    

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Renvoyer l'utilisateur actuellement connecté
        return self.request.user

class TechnicienView(generics.RetrieveUpdateAPIView):
    queryset = Technicien.objects.all()
    serializer_class = TechnicienSerializer
    permission_classes = []

    def get_object(self):
        # Renvoyer le technicien actuellement connecté
        return self.request.user.technicien
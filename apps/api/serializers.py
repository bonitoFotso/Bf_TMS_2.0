from rest_framework import serializers
from apps.project.models import Tache,Categorie, Activite,TechnicienTache
from apps.clients.models import  Appelant,Client,Agence
from apps.ressource.models import Technicien
from account.models import User



class TechnicienTacheSerialiser(serializers.ModelSerializer):
    class Meta:
        model = TechnicienTache
        fields = ('technicien',)

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'  # Incluez tous les champs du modèle dans la sérialisation
        

class ActiviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activite
        fields = ('id', 'nom', 'description')

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ('id', 'nom', 'description')

class AgenceSerializer(serializers.ModelSerializer):
    siege = ClientSerializer()

    class Meta:
        model = Agence
        fields = '__all__'


class AppelantSerializer(serializers.ModelSerializer):
    agence = AgenceSerializer()
    class Meta:
        model = Appelant
        fields = '__all__'

class TechnicienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technicien
        fields = '__all__'



class TacheSerializer(serializers.ModelSerializer):
    activite = ActiviteSerializer(many=True)
    categorie = CategorieSerializer(many=True)
    appelant = AppelantSerializer()
    assignations = TechnicienSerializer(many=True)

    class Meta:
        model = Tache
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email','profile', 'name', 'is_helpdesk', 'is_technicien', 'active', 'staff', 'admin', 'timestamp', 'is_manager', 'is_team_leader','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            #username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class TSerializer(serializers.ModelSerializer):
    # Ajoutez ces champs pour gérer les relations many-to-many
    activite = serializers.PrimaryKeyRelatedField(queryset=Activite.objects.all(), many=True)
    categorie = serializers.PrimaryKeyRelatedField(queryset=Categorie.objects.all(), many=True)
    assignations = serializers.PrimaryKeyRelatedField(queryset=Technicien.objects.all(), write_only=True, many=True)

    class Meta:
        model = Tache
        fields = '__all__'

    def create(self, validated_data):
        # Récupérez les techniciens à partir des données validées
        assignations_data = validated_data.pop('assignations', [])
        activites_data = validated_data.pop('activite', [])
        categories_data = validated_data.pop('categorie', [])

        # Créez la tâche
        tache = Tache.objects.create(**validated_data)

        # Ajoutez les techniciens à la tâche
        tache.assignations.set(assignations_data)
        tache.activite.set(activites_data)
        tache.categorie.set(categories_data)

        #for technicien in assignations_data:
        #    TechnicienTache.objects.create(tache=tache, technicien=technicien)

        return tache

    def update(self, instance, validated_data):
        # Mettez à jour les champs de base de la tâche
        instance.nom = validated_data.get('nom', instance.nom)
        instance.status = validated_data.get('status', instance.status)
        instance.appelant = validated_data.get('appelant', instance.appelant)
        instance.priorite = validated_data.get('priorite', instance.priorite)
        instance.description = validated_data.get('description', instance.description)
        instance.n_OS = validated_data.get('n_OS', instance.n_OS)
        instance.date_debut = validated_data.get('date_debut', instance.date_debut)
        instance.date_fin = validated_data.get('date_fin', instance.date_fin)

        # Mettez à jour les relations many-to-many (activite, categorie)
        instance.activite.set(validated_data.get('activite', instance.activite.all()))
        instance.categorie.set(validated_data.get('categorie', instance.categorie.all()))

        # Mettez à jour les relations many-to-many (assignations)
        assignations_data = validated_data.get('assignations', [])
        TechnicienTache.objects.filter(tache=instance).delete()
        for technicien in assignations_data:
            TechnicienTache.objects.create(tache=instance, technicien=technicien)

        instance.save()
        return instance


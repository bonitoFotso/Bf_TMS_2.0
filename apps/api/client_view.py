from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Count
from apps.clients.models import  Appelant,Client,Agence
from .serializers import (AppelantSerializer,ClientSerializer,AgenceSerializer,)
from rest_framework.views import APIView
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from datetime import datetime, timedelta


class ClientDetailViewData(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Sérialiser le client
        client_data = ClientSerializer(instance).data

        # Récupérer les agences associées au client
        agences = Agence.objects.filter(siege=instance)
        agences_data = AgenceSerializer(agences, many=True).data

        # Récupérer les appelants associés au client
        appelants = Appelant.objects.filter(agence__in=agences)
        appelants_data = AppelantSerializer(appelants, many=True).data

        # Compter le nombre d'agences et d'appelants associés au client
        agence_count = agences.count()
        appelant_count = Appelant.objects.filter(agence__in=agences).count()

        # Répartition des agences par adresse et ville
        agences_by_address = agences.values('address').annotate(count=Count('id'))
        agences_by_city = agences.values('city').annotate(count=Count('id'))

        response_data = {
            'client': client_data,
            'agences': agences_data,
            'appelants': appelants_data,
            'agences_by_address': agences_by_address,
            'agences_by_city': agences_by_city,
            'agence_count': agence_count,
            'appelant_count': appelant_count,

        }

        return Response(response_data)

@method_decorator(cache_page(60 * 2), name='dispatch')  # Cache la réponse pendant 2 minutes
class ClientAgenceChart(APIView):
    def get(self, request, format=None):
        # Répartition des agences par clients
        client_agence_data = Client.objects.values('name').annotate(agence_count=Count('agence'))

        # Répartition des agences par adresse
        address_data = Agence.objects.values('address').annotate(agence_count=Count('id'))

        # Répartition des agences par ville
        city_data = Agence.objects.values('city').annotate(agence_count=Count('id'))

        # Nombre d'agences au cours du temps
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # Sur une année
        monthly_data = Agence.objects.filter(createdAt__range=(start_date, end_date))\
            .annotate(month=TruncMonth('createdAt'))\
            .values('month')\
            .annotate(agence_count=Count('id'))

        data = {
            'client_agence_data': client_agence_data,
            'address_data': address_data,
            'city_data': city_data,
            'monthly_data': monthly_data,
        }

        return Response(data)

class ClientChartDataView(APIView):
    def get(self, request, format=None):
        try:
            # Répartition par adresse
            address_data = Client.objects.values('address').annotate(client_count=Count('id'))
            client_agence_data = Client.objects.values('name').annotate(agence_count=Count('agence'))

            # Nombre de clients sous contrat et non sous contrat
            contracted_clients = Client.objects.filter(maintenance=True).count()
            non_contracted_clients = Client.objects.filter(maintenance=False).count()

            # Évolution du nombre de clients au fil du temps (par mois)
            current_month = timezone.now()
            twelve_months_ago = current_month - timezone.timedelta(days=365)
            monthly_data = Client.objects.filter(createdAt__range=[twelve_months_ago, current_month]) \
                .annotate(month=TruncMonth('createdAt')) \
                .values('month') \
                .annotate(client_count=Count('id'))

            response_data = {
                "address_data": address_data,
                "contracted_clients": contracted_clients,
                "non_contracted_clients": non_contracted_clients,
                "monthly_data": monthly_data,
                "client_agence_data": client_agence_data,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class AgenceChartDataView(APIView):
    def get(self, request, format=None):
        # Retrieve data for charts (e.g., count of agencies per city)
        data = Agence.objects.values('city').annotate(agence_count=Count('id'))
        return Response(data, status=status.HTTP_200_OK)
    
class AppelantChartDataView(APIView):
    def get(self, request, format=None):
        # Retrieve data for charts (e.g., count of appellants per agency)
        data = Appelant.objects.values('agence__name').annotate(appelant_count=Count('id'))
        return Response(data, status=status.HTTP_200_OK)
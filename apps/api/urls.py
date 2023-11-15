from django.urls import path
from .views import (
    
    CategorieListCreateView,
    CategorieDetailView,
    ActiviteListCreateView,
    ActiviteDetailView,
    AppelantListCreateView,
    AppelantDetailView,
    ClientListCreateView,
    ClientDetailView,
    AgenceListCreateView,
    AgenceDetailView,
    TechnicienListCreateView,
    TechnicienDetailView,
    UserProfileView,
    TechnicienView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .client_view import ClientChartDataView,ClientAgenceChart,ClientDetailViewData
from .auth_views import *
from .tache_views import (TacheListCreateView,TacheDetailView, AllView, TacheCreateView )

urlpatterns = [
    path("taches/", TacheListCreateView.as_view(), name="tache-list-create"),
    path("taches-c/", TacheCreateView.as_view(), name="tache-create"),

    path("taches/<int:pk>", TacheDetailView.as_view(), name="taches-detail"),
    path("all/", AllView.as_view(), name="all"),

    path(
        "categories/", CategorieListCreateView.as_view(), name="categorie-list-create"
    ),
    path(
        "categories/<int:pk>/", CategorieDetailView.as_view(), name="categorie-detail"
    ),
    path("activites/", ActiviteListCreateView.as_view(), name="activite-list-create"),
    path("activites/<int:pk>/", ActiviteDetailView.as_view(), name="activite-detail"),
    path("appelants/", AppelantListCreateView.as_view(), name="appelant-list-create"),
    path("appelants/<int:pk>/", AppelantDetailView.as_view(), name="appelant-detail"),
    # URL pour les vues de la client
    path("clients/", ClientListCreateView.as_view(), name="client-list-create"),
    path("clients_data/", ClientChartDataView.as_view(), name="client-data"),
    path('clients_agence_data/', ClientAgenceChart.as_view(), name='agence-chart-data'),
    path("clients_agence/<int:pk>/", ClientDetailViewData.as_view(), name="client-detail-data"),
    path("clients/<int:pk>/", ClientDetailView.as_view(), name="client-detail"),
    # URL pour les vues de l'agence
    path("agences/", AgenceListCreateView.as_view(), name="agence-list-create"),
    path("agences/<int:pk>/", AgenceDetailView.as_view(), name="agence-detail"),
    path(
        "techniciens/",
        TechnicienListCreateView.as_view(),
        name="technicien-list-create",
    ),
    path(
        "techniciens/<int:pk>/",
        TechnicienDetailView.as_view(),
        name="technicien-detail",
    ),
    #
    path("login/", LoginApi.as_view()),
    path("register/", RegisterApi.as_view()),
    # Ajoutez des URL similaires pour les modèles Agence et Appelant si nécessaire
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", TechnicienView.as_view(), name="profile"),
]

from django.shortcuts import render,redirect
from django.views.generic import *
from django.urls import reverse_lazy
from .models import *
from django.http import JsonResponse

# Register your models here.

# views.py
from django.views.generic import ListView, CreateView,View
from .models import Client, Agence, Appelant
from .forms import ClientForm, AgenceForm, AppelantForm


class ClientView(View):
    template_name = 'clients/clients.html'
    
    def get_context_data(self, **kwargs):
        context ={}
        context["title"] = "Client"
        context['form'] = ClientForm()
        return context
    

    def get(self, request):
        breadcrumb = [{'label': 'Accueil', 'url': '/'}]  # Le breadcrumb de base
        breadcrumb.append({'label': 'Client', 'url': '/clients'})  # Ajoutez les éléments au breadcrumb
        request.breadcrumb = breadcrumb  # Ajoutez le breadcrumb au contexte
        context = self.get_context_data()
        clients = Client.objects.all()
        agences = Agence.objects.all()
        context['clients'] = clients
        context['agences'] = agences

        return render(request, self.template_name, context)

    def post(self, request):
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients')  # Rediriger vers la liste des clients
        return render(request, self.template_name, {'form': form})
    
    

def get_client_data(request):
    clients = Client.objects.all()

    # Créez une liste de dictionnaires pour stocker les données de chaque client
    client_data = []

    for client in clients:
        client_data.append({
            'name': client.name,
            'responsable': client.responsable,
            'email': client.email,
            'phone': client.phone,
            'address': client.address,
            'city': client.city,
            'n_client': client.n_client,
            'maintenance': client.maintenance,
            #'createdAt': client.createdAt.strftime('%Y-%m-%d %H:%M:%S'), # Formatage de la date
            #'updatedAt': client.updatedAt.strftime('%Y-%m-%d %H:%M:%S'), # Formatage de la date
        })

    # Renvoyez les données au format JSON
    return JsonResponse({'data': client_data})

class ClientListView(ListView):
    model = Client
    template_name = 'client_list.html'
    context_object_name = 'clients'

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client_form.html'
    success_url = '/client-list/'

class AgenceListView(ListView):
    model = Agence
    template_name = 'agence_list.html'
    context_object_name = 'agences'

class AgenceCreateView(CreateView):
    model = Agence
    form_class = AgenceForm
    template_name = 'agence_form.html'
    success_url = '/agence-list/'

class AppelantListView(ListView):
    model = Appelant
    template_name = 'appelant_list.html'
    context_object_name = 'appelants'

class AppelantCreateView(CreateView):
    model = Appelant
    form_class = AppelantForm
    template_name = 'appelant_form.html'
    success_url = '/appelant-list/'

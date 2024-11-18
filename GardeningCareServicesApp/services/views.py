from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from GardeningCareServicesApp.accounts.models import ServiceProviderProfile
from GardeningCareServicesApp.services.forms import ServiceAddForm
from GardeningCareServicesApp.services.models import Service


# Create your views here.

class ServicesListPage(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = 10


class ServiceAddPage(CreateView):
    model = Service
    template_name = 'services/service_create.html'
    form_class = ServiceAddForm
    success_url = reverse_lazy('services-list')

    def form_valid(self, form):
        service = form.save(commit=False)
        provider_profile = ServiceProviderProfile.objects.get(user=self.request.user)
        service.provider = provider_profile

        return super().form_valid(form)

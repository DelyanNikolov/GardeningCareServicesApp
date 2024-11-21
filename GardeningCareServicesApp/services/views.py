from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from GardeningCareServicesApp.accounts.models import ServiceProviderProfile, HomeOwnerProfile
from GardeningCareServicesApp.common.forms import ReviewForm
from GardeningCareServicesApp.services.forms import ServiceAddForm, ServiceEditForm
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


class ServiceDetailsPage(DetailView):
    model = Service
    template_name = 'services/service_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        # Calculate full stars and empty stars for each review
        reviews = self.object.service_reviews.all()
        context['reviews_with_stars'] = [
            {
                'review': review,
                'filled_stars': range(review.rating),
                'empty_stars': range(5 - review.rating)
            }
            for review in reviews
        ]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.service = self.object
            review.user = HomeOwnerProfile.objects.get(user=self.request.user)
            review.save()
            return redirect(reverse('service-details', args=[self.object.id]))

        context = self.get_context_data()
        context['review_form'] = form
        return self.render_to_response(context)


class ServiceEditPage(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceEditForm
    template_name = 'services/service_edit.html'

    def get_object(self, queryset=None):
        service = get_object_or_404(Service, pk=self.kwargs['pk'])

        if service.provider.user != self.request.user:
            raise PermissionDenied("You are not authorized to edit this service.")
        return service

    def get_success_url(self):
        service = get_object_or_404(Service, pk=self.kwargs['pk'])
        return reverse_lazy('provider-profile', kwargs={'pk': service.provider.pk})


class ServiceDeletePage(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'services/service_delete.html'
    success_url = reverse_lazy('services-list')

    def get_object(self, queryset=None):
        service = super().get_object(queryset)

        if service.provider.user != self.request.user:
            raise PermissionDenied("You are not authorized to delete this service.")
        return service

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from GardeningCareServicesApp.accounts.models import ServiceProviderProfile
from GardeningCareServicesApp.providers.fomrs import ServiceProviderProfileForm


# Create your views here.


class ProvidersListPage(ListView):
    model = ServiceProviderProfile
    template_name = 'providers/providers_list.html'
    context_object_name = 'providers'

    def get_queryset(self):
        # Update average ratings for each provider
        providers = ServiceProviderProfile.objects.all()
        for provider in providers:
            provider.update_average_rating()
        return providers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        providers = context['providers']

        # Prepare star data for each provider
        context['providers_with_stars'] = [
            {
                'provider': provider,
                'filled_stars': range(int(provider.rating)),
                'empty_stars': range(5 - int(provider.rating)),
            }
            for provider in providers
        ]
        return context


class ProviderProfilePage(DetailView):
    model = ServiceProviderProfile
    template_name = 'providers/provider_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object

        # Calculate star ratings for the provider
        filled_stars = int(profile.rating)
        empty_stars = 5 - filled_stars

        # Add services provided by the provider
        services = profile.provider_services.all()

        # Determine if the current user is the owner of the profile, or it has permission to change the profile
        is_owner = self.request.user == profile.user or self.request.user.has_perm(
            'accounts.change_serviceproviderprofile'
        )

        context.update({
            'filled_stars': range(filled_stars),
            'empty_stars': range(empty_stars),
            'services': services,
            'is_owner': is_owner,
        })
        return context


class ProviderEditPage(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ServiceProviderProfile
    template_name = 'providers/provider_edit.html'
    form_class = ServiceProviderProfileForm
    permission_required = 'accounts.change_serviceproviderprofile'

    def get_object(self, queryset=None):
        # Allow access if the user is the profile owner or has the required permission
        profile = get_object_or_404(ServiceProviderProfile, pk=self.kwargs['pk'])
        if self.request.user != profile.user and not self.request.user.has_perm(self.permission_required):
            raise PermissionDenied("You are not authorized to edit this profile.")
        return profile

    def form_valid(self, form):
        # Save the profile and redirect to the profile page
        self.object = form.save()
        return redirect(reverse('provider-profile', kwargs={'pk': self.object.pk}))


class ProfileDeletePage(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ServiceProviderProfile
    template_name = 'providers/profile_delete_confirm.html'
    success_url = reverse_lazy('home')  # Redirect to the home page after deletion
    permission_required = 'accounts.delete_serviceproviderprofile'

    def get_object(self, queryset=None):
        profile = get_object_or_404(ServiceProviderProfile, pk=self.kwargs['pk'])
        if self.request.user != profile.user and not self.request.user.has_perm(self.permission_required):
            raise PermissionDenied("You are not authorized to delete this profile.")
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object  # Pass the profile object
        return context

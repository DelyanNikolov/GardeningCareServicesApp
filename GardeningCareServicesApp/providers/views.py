from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from GardeningCareServicesApp.accounts.models import ServiceProviderProfile
# Create your views here.

from GardeningCareServicesApp.providers.fomrs import ServiceProviderProfileForm


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

        # Determine if the current user is the owner of the profile
        is_owner = self.request.user == profile.user

        context.update({
            'filled_stars': range(filled_stars),
            'empty_stars': range(empty_stars),
            'services': services,
            'is_owner': is_owner,
        })
        return context


class ProviderEditPage(UpdateView):
    template_name = 'providers/provider_edit.html'

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(ServiceProviderProfile, user=request.user)
        form = ServiceProviderProfileForm(instance=profile)
        return self.render_to_response({'form': form, 'profile': profile})

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(ServiceProviderProfile, user=request.user)
        form = ServiceProviderProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('provider-profile', kwargs={'pk': profile.pk}))
        return self.render_to_response({'form': form, 'profile': profile})


class ProfileDeletePage(DeleteView):
    model = ServiceProviderProfile
    template_name = 'providers/profile_delete_confirm.html'
    success_url = reverse_lazy('home')  # Redirect to the home page after deletion

    def get_object(self, queryset=None):
        # Ensure the logged-in user can only delete their own profile
        return get_object_or_404(ServiceProviderProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object  # Pass the profile object
        return context

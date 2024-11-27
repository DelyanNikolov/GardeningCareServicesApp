from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, DetailView

from GardeningCareServicesApp.accounts.models import HomeOwnerProfile
from GardeningCareServicesApp.homeowners.forms import HomeOwnerProfileForm


class HomeOwnerProfilePage(DetailView):
    model = HomeOwnerProfile
    template_name = 'homeowners/homeowner_profile.html'
    context_object_name = 'profile'


class HomeOwnerProfileEditPage(LoginRequiredMixin, UpdateView):
    model = HomeOwnerProfile
    form_class = HomeOwnerProfileForm
    template_name = 'homeowners/homeowner_edit.html'

    def get_object(self, queryset=None):
        # Ensure the logged-in user can only edit their own profile
        return get_object_or_404(HomeOwnerProfile, user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('homeowner-profile', kwargs={'pk': self.object.pk})


class HomeOwnerProfileDeletePage(LoginRequiredMixin, DeleteView):
    model = HomeOwnerProfile
    template_name = 'homeowners/homeowner_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        # Ensure the logged-in user can only delete their own profile
        return get_object_or_404(HomeOwnerProfile, user=self.request.user)

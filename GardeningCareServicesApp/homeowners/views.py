from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
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
    permission_required = 'homeowners.change_profile'
    model = HomeOwnerProfile
    form_class = HomeOwnerProfileForm
    template_name = 'homeowners/homeowner_edit.html'

    def get_object(self, queryset=None):
        # Allow access if the user is the profile owner or has the required permission
        profile = get_object_or_404(HomeOwnerProfile, pk=self.kwargs['pk'])
        if self.request.user != profile.user and not self.request.user.has_perm(self.permission_required):
            raise PermissionDenied("You are not authorized to edit this profile.")
        return profile

    def get_success_url(self):
        return reverse_lazy('homeowner-profile', kwargs={'pk': self.object.pk})


class HomeOwnerProfileDeletePage(LoginRequiredMixin, DeleteView):
    permission_required = 'homeowners.delete_profile'
    model = HomeOwnerProfile
    template_name = 'homeowners/homeowner_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        # Allow access if the user is the profile owner or has the required permission
        profile = get_object_or_404(HomeOwnerProfile, pk=self.kwargs['pk'])
        if self.request.user != profile.user and not self.request.user.has_perm(self.permission_required):
            raise PermissionDenied("You are not authorized to edit this profile.")
        return profile

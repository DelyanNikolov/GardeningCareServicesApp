from django import forms

from GardeningCareServicesApp.services.models import Service


class ServiceAddForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'category', 'price', 'photo']


class ServiceEditForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'category', 'price', 'photo']

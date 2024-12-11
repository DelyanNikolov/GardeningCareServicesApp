from django import forms

from GardeningCareServicesApp.services.models import Service, ServiceCategory


class BaseServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'category', 'price', 'photo']
        help_texts = {
            'photo': 'File limit: 1MB',
        }


class ServiceAddForm(BaseServiceForm):
    pass


class ServiceEditForm(BaseServiceForm):
    pass


class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ['name', 'description', ]

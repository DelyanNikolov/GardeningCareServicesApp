from django import forms


from GardeningCareServicesApp.accounts.models import ServiceProviderProfile


class ServiceProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ServiceProviderProfile
        fields = ['business_name', 'service_description', 'location', 'phone_number', 'years_of_experience']


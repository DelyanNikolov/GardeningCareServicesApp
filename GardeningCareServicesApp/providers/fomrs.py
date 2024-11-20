from django import forms


from GardeningCareServicesApp.accounts.models import ServiceProviderProfile


class ServiceProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ServiceProviderProfile
        fields = ['business_name', 'service_description', 'location', 'years_of_experience']
        widgets = {
            'business_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-sm',
                'placeholder': 'Enter your business name'
            }),
            'service_description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-sm',
                'placeholder': 'Describe the services you offer',
                'rows': 4
            }),
            'location': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-sm',
                'placeholder': 'Enter your location'
            }),
            'years_of_experience': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-sm',
                'placeholder': 'Enter years of experience'
            }),
        }


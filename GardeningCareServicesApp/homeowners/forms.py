from django import forms

from GardeningCareServicesApp.accounts.models import HomeOwnerProfile


class HomeOwnerProfileForm(forms.ModelForm):
    class Meta:
        model = HomeOwnerProfile
        fields = ['first_name', 'last_name', 'address', 'phone_number']

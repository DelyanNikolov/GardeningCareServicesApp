from django import forms

from GardeningCareServicesApp.services.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')

        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Add comment...'}),
        }

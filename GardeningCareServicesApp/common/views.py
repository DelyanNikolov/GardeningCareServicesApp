from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView


def custom_home_view(request):
    # Check if the user is an administrator or staff
    if request.user.groups.filter(name="Administrator").exists() or request.user.is_staff:
        return redirect(reverse('moderation-dashboard'))

    # Redirect other users to the regular home page
    return redirect(reverse('public-home'))


# Create your views here.
class PublicIndexView(TemplateView):
    template_name = 'common/home.html'

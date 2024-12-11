from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView


# Create your views here.

def custom_home_view(request):
    # Check if the user is an administrator or staff
    if (request.user.groups.filter(name='Administrators').exists()
            or request.user.groups.filter(name='Moderators').exists()
            or request.user.is_staff):
        return redirect(reverse('moderation-dashboard'))

    # Redirect other users to the regular home page
    return redirect(reverse('public-home'))


class PublicIndexView(TemplateView):
    # Public page for unauthenticated and users with no special permissions
    template_name = 'common/home.html'

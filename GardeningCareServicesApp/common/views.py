from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class IndexView(TemplateView):
    def get_template_names(self, **kwargs):
        if self.request.user.groups.filter(name='Moderator').exists() or self.request.user.is_staff:
            return ['services/moderation_dashboard.html']
        else:
            return ['common/home.html']

from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from GardeningCareServicesApp.accounts.forms import AppUserCreationForm

# Create your views here.

UserModel = get_user_model()


class LoginPage(LoginView):
    template_name = 'accounts/login.html'


class RegisterPage(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        return response

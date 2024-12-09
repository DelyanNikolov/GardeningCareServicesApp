from django.contrib.auth.views import LogoutView
from django.urls import path

from GardeningCareServicesApp.accounts.views import LoginPage, RegisterPage

urlpatterns = [
    path('login/', LoginPage.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
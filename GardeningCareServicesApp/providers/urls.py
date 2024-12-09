from django.urls import path

from GardeningCareServicesApp.providers.views import ProvidersListPage, ProviderProfilePage, ProviderEditPage, \
    ProfileDeletePage

urlpatterns = [
    path('', ProvidersListPage.as_view(), name='providers-list'),
    path('<int:pk>/', ProviderProfilePage.as_view(), name='provider-profile'),
    path('profile/edit/<int:pk>/', ProviderEditPage.as_view(), name='provider-edit'),
    path('profile/delete/<int:pk>/', ProfileDeletePage.as_view(), name='profile-delete'),
]

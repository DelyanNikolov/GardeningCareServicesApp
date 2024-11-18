from django.urls import path

from GardeningCareServicesApp.services.views import ServicesListPage, ServiceAddPage

urlpatterns = [
    path('', ServicesListPage.as_view(), name='services-list'),
    path('create/', ServiceAddPage.as_view(), name='services-create'),
]

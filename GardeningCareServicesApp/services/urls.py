from django.urls import path, include

from GardeningCareServicesApp.services.views import ServicesListPage, ServiceAddPage, ServiceDetailsPage

urlpatterns = [
    path('', ServicesListPage.as_view(), name='services-list'),
    path('create/', ServiceAddPage.as_view(), name='services-create'),
    path('<int:pk>/', include([
        path('details/', ServiceDetailsPage.as_view(), name='service-details'),
    ])),
]

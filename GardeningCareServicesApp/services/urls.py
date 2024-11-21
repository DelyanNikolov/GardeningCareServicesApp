from django.urls import path, include

from GardeningCareServicesApp.services.views import ServicesListPage, ServiceAddPage, ServiceDetailsPage, \
    ServiceEditPage, ServiceDeletePage

urlpatterns = [
    path('', ServicesListPage.as_view(), name='services-list'),
    path('create/', ServiceAddPage.as_view(), name='services-create'),
    path('<int:pk>/', include([
        path('details/', ServiceDetailsPage.as_view(), name='service-details'),
        path('edit/', ServiceEditPage.as_view(), name='service-edit'),
        path('delete/', ServiceDeletePage.as_view(), name='service-delete'),
    ])),
]

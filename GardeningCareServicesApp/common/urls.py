from django.urls import path

from GardeningCareServicesApp.common.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
]


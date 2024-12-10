from django.urls import path

from GardeningCareServicesApp.common.views import PublicIndexView, custom_home_view

urlpatterns = [
    path('', custom_home_view, name='home'),
    path('index/', PublicIndexView.as_view(), name='public-home'),
]


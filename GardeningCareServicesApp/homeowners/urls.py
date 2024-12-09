from django.urls import path

from GardeningCareServicesApp.homeowners.views import HomeOwnerProfileEditPage, \
    HomeOwnerProfileDeletePage, HomeOwnerProfilePage

urlpatterns = [
    path('<int:pk>/', HomeOwnerProfilePage.as_view(), name='homeowner-profile'),
    path('<int:pk>/edit/', HomeOwnerProfileEditPage.as_view(), name='homeowner-profile-edit'),
    path('<int:pk>/delete/', HomeOwnerProfileDeletePage.as_view(), name='homeowner-profile-delete'),
]
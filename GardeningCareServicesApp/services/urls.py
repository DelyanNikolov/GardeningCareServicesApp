from django.urls import path, include
from rest_framework.routers import DefaultRouter

from GardeningCareServicesApp.services.views import ServicesListPage, ServiceAddPage, ServiceDetailsPage, \
    ServiceEditPage, ServiceDeletePage, moderation_dashboard, approve_review, delete_review, ServiceCategoryViewSet

router = DefaultRouter()
router.register(r'categories', ServiceCategoryViewSet, basename='servicecategory')

urlpatterns = [
    path('', ServicesListPage.as_view(), name='services-list'),
    path('create/', ServiceAddPage.as_view(), name='services-create'),
    path('moderation/', include([
        path('', moderation_dashboard, name='moderation-dashboard'),
        path('moderation/reviews/<int:pk>/approve/', approve_review, name='approve-review'),
        path('moderation/reviews/<int:pk>/delete/', delete_review, name='delete-review'),
    ])),
    path('<int:pk>/', include([
        path('details/', ServiceDetailsPage.as_view(), name='service-details'),
        path('edit/', ServiceEditPage.as_view(), name='service-edit'),
        path('delete/', ServiceDeletePage.as_view(), name='service-delete'),
    ])),
    path('api/', include(router.urls)),  # Add API URLs here for category management
]

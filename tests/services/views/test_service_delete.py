from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from GardeningCareServicesApp.accounts.models import ServiceProviderProfile
from GardeningCareServicesApp.services.models import Service, ServiceCategory

UserModel = get_user_model()


class TestServiceDelete(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name='Test Category', description='Test Category')

        self.user = UserModel.objects.create_user(
            email='test@test.com',
            password='password',
            user_type='Service Provider'
        )

        self.other_user = UserModel.objects.create_user(
            email='test2@test.com',
            password='password',
            user_type='Service Provider'
        )

        self.service = Service.objects.create(
            photo="photo.png",
            name="Test Service",
            description="Test Service Description",
            price=10,
            provider=ServiceProviderProfile.objects.filter(pk=self.user.pk).first(),
            category=self.category,
        )

        self.client.login(
            email='test@test.com',
            password='password'
        )

    def test_service_delete_when_user_is_owner_expect_success(self):
        self.assertTrue(Service.objects.filter(pk=self.service.pk).exists())

        response = self.client.post(
            reverse('service-delete', kwargs={'pk': self.service.pk}),
        )

        self.assertFalse(Service.objects.filter(pk=self.service.pk).exists())
        self.assertRedirects(response, reverse('services-list'))

    def test_service_delete_when_user_is_not_owner_expect_photo_not_deleted(self):
        self.client.login(
            email='test2@test.com',
            password='password'
        )

        response = self.client.post(
            reverse('service-delete', kwargs={'pk': self.service.pk}),
        )

        self.assertTrue(Service.objects.filter(pk=self.service.pk).exists())
        self.assertEqual(response.status_code, 403)

    def test_service_delete_with_anonymous_user_expect_redirect_to_login(self):
        self.client.logout()

        response = self.client.post(
            reverse('service-delete', kwargs={'pk': self.service.pk}),
        )

        self.assertTrue(Service.objects.filter(pk=self.service.pk).exists())

        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('service-delete', kwargs={'pk': self.service.pk})}")

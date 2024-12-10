from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse

from GardeningCareServicesApp.accounts.models import ServiceProviderProfile, HomeOwnerProfile
from GardeningCareServicesApp.services.models import ServiceCategory, Service, Review

UserModel = get_user_model()


class TestApproveReview(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name='Test Category', description='Some description')

        self.homeowner = UserModel.objects.create_user(
            email='homeowner@test.com',
            password='password',
        )

        self.provider = UserModel.objects.create_user(
            email='provider@test.com',
            password='password',
            user_type='Service Provider'
        )

        self.service = Service.objects.create(
            photo="photo.png",
            name="Test Service",
            description="Test Service Description",
            price=10,
            provider=ServiceProviderProfile.objects.filter(pk=self.provider.pk).first(),
            category=self.category,
        )

        self.review = Review.objects.create(
            service=self.service,
            user=HomeOwnerProfile.objects.filter(pk=self.homeowner.pk).first(),
            rating=4,
            comment="Great service!"
        )

    def test_anonymous_user_gives_comment_expected_redirect(self):
        response = self.client.post(
            reverse('moderation-dashboard'),
        )

        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('moderation-dashboard')}"
        )

    def test_logged_in_user_without_permission_expect_permission_denied(self):
        # Log in as a regular user without the required permission
        self.client.login(email='testuser@test.com', password='testpass')

        response = self.client.post(
            reverse('moderation-dashboard'),
        )

        self.assertRaises(PermissionDenied)

    def test_approve_review_with_permission(self):
        # Grant the 'change_review' permission to the user
        self.homeowner.user_permissions.add(Permission.objects.get(codename='change_review'))

        # Ensure user has permission
        self.assertTrue(self.homeowner.has_perm('services.change_review'))

        # Log in as the user
        self.client.login(email='homeowner@test.com', password='testpass')

        # Access the view
        url = reverse('approve-review', args=[self.review.pk])
        response = self.client.post(url)

        # Check response status code
        self.assertEqual(response.status_code, 302)

        # Reload the review from the database
        print(f"Before: {self.review.is_approved}")
        self.review.refresh_from_db()
        print(f"After: {self.review.is_approved}")

        # Verify the review is approved
        self.assertTrue(self.review.is_approved)

        # Verify redirection to the moderation dashboard
        self.assertRedirects(response, reverse('moderation-dashboard'))


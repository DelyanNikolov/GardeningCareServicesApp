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
        # Create category
        self.category = ServiceCategory.objects.create(name='Test Category', description='Some description')

        # Create homeowner and associated profile
        self.homeowner = UserModel.objects.create_user(
            email='homeowner@test.com',
            password='password',
        )
        self.homeowner_profile, created = HomeOwnerProfile.objects.get_or_create(user=self.homeowner)

        # Create service provider and associated profile
        self.provider = UserModel.objects.create_user(
            email='provider@test.com',
            password='password',
            user_type='Service Provider'
        )
        self.provider_profile, created = ServiceProviderProfile.objects.get_or_create(user=self.provider)

        # Create service
        self.service = Service.objects.create(
            photo="photo.png",
            name="Test Service",
            description="Test Service Description",
            price=10,
            provider=self.provider_profile,
            category=self.category,
        )

        # Create review
        self.review = Review.objects.create(
            service=self.service,
            user=self.homeowner_profile,
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

    from django.contrib.auth.models import Permission

    def test_approve_review_with_permission(self):
        # Grant the 'change_review' permission
        permission1 = Permission.objects.get(codename='change_review')
        permission2 = Permission.objects.get(codename='view_review')
        self.homeowner.user_permissions.add(permission1)
        self.homeowner.user_permissions.add(permission2)

        # Verify the user has the permission
        self.assertTrue(self.homeowner.has_perm('services.change_review'))
        self.assertTrue(self.homeowner.has_perm('services.view_review'))

        # Log in as the user
        self.client.login(email='homeowner@test.com', password='password')

        # Access the approve-review view
        url = reverse('approve-review', args=[self.review.pk])
        response = self.client.post(url)

        # Reload the review from the database
        self.review.refresh_from_db()

        # Check if the review is approved
        self.assertTrue(self.review.is_approved)

        # Verify redirection to the moderation dashboard
        self.assertRedirects(response, reverse('moderation-dashboard'))

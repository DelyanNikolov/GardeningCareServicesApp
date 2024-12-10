from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.exceptions import PermissionDenied

from GardeningCareServicesApp.accounts.models import HomeOwnerProfile, ServiceProviderProfile
from GardeningCareServicesApp.common.forms import ReviewForm
from GardeningCareServicesApp.services.models import ServiceCategory, Service, Review

User = get_user_model()


class ServiceDetailsPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user and a homeowner profile
        cls.user = User.objects.create_user(email="testuser@test.com", password="testpass")
        cls.user2 = User.objects.create_user(email="testuser1@test.com", password="testpass", user_type="Service Provider")
        cls.user3 = User.objects.create_user(email="testuser3@test.com", password="testpass")
        cls.homeowner = HomeOwnerProfile.objects.filter(pk=cls.user.pk).first()
        cls.provider = ServiceProviderProfile.objects.filter(pk=cls.user2.pk).first()

        # Create a service category and service
        cls.category = ServiceCategory.objects.create(name="Plumbing", description="All plumbing services.")
        cls.service = Service.objects.create(
            name="Pipe Fixing",
            description="Fixing broken pipes.",
            category=cls.category,
            provider=cls.provider,
            price=100.00,
        )

        # Create a review
        cls.review = Review.objects.create(
            service=cls.service,
            user=cls.homeowner,
            rating=4,
            comment="Great service!"
        )

    def test_get_context_data(self):
        url = reverse('service-details', args=[self.service.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services/service_detail.html')
        self.assertIsInstance(response.context['review_form'], ReviewForm)

        # Check if reviews with stars are correctly populated
        reviews_with_stars = response.context['reviews_with_stars']
        self.assertEqual(len(reviews_with_stars), 1)
        self.assertEqual(reviews_with_stars[0]['filled_stars'], range(4))
        self.assertEqual(reviews_with_stars[0]['empty_stars'], range(1))

    def test_post_review_authenticated_homeowner_expected_new_post_created_success_msg(self):
        self.client.login(email="testuser3@test.com", password="testpass")
        url = reverse('service-details', args=[self.service.id])

        # Post a new review
        data = {'rating': 5, 'comment': "Excellent!"}
        response = self.client.post(url, data)

        # Check the review is created
        self.assertEqual(Review.objects.count(), 2)
        self.assertRedirects(response, url)

        # Verify success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Your review has been submitted." in str(message) for message in messages))

    from django.core.exceptions import PermissionDenied

    def test_post_review_non_authenticated_user_expect_403_Forbidden(self):
        url = reverse('service-details', args=[self.service.id])

        # Post a review without logging in
        data = {'rating': 5, 'comment': "Unauthorized!"}

        # Make the post request
        response = self.client.post(url, data)

        # Assert that the response status code is 403
        self.assertEqual(response.status_code, 403)

    def test_post_review_non_homeowner_expected_error_msg(self):
        non_homeowner = User.objects.create_user(email="otheruser@test.com", password="testpass", user_type="Service Provider")
        self.client.login(email="otheruser@test.com", password="testpass")
        url = reverse('service-details', args=[self.service.id])

        # Post a review
        data = {'rating': 3, 'comment': "Not allowed"}
        response = self.client.post(url, data)

        # Check the user is redirected with an error message
        self.assertRedirects(response, url)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Only homeowners can leave reviews." in str(message) for message in messages))

    def test_post_duplicate_review_expected_no_review_created_and_error_msg(self):
        self.client.login(email="testuser@test.com", password="testpass")
        url = reverse('service-details', args=[self.service.id])

        # Post a duplicate review
        data = {'rating': 5, 'comment': "Duplicate review"}
        response = self.client.post(url, data)

        # Check that no new review is created
        self.assertEqual(Review.objects.count(), 1)

        # Verify error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("You have already reviewed this service." in str(message) for message in messages))

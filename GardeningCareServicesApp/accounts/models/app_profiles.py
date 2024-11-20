from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

UserModel = get_user_model()


class ServiceProviderProfile(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    business_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    service_description = models.TextField(
        blank=True,
        null=True
    )

    # the average rating of the provider
    rating = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ],
    )

    location = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    years_of_experience = models.PositiveIntegerField(
        default=0
    )

    def update_average_rating(self):
        """Calculate and update the average rating based on all services for this provider."""
        services = self.provider_services.all()  # Use related_name for the Service model's provider field
        if services.exists():
            self.rating = services.aggregate(models.Avg('service_reviews__rating'))[
                              'service_reviews__rating__avg'] or 0.0
        else:
            self.rating = 0.0
        self.save()

    def __str__(self):
        return f"Service Provider Profile for {self.user.email}"


class HomeOwnerProfile(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name

        return self.first_name or self.last_name or "Anonymous"

    def __str__(self):
        return f"Homeowner Profile for {self.user.email}"

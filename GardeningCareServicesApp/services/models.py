from django.db import models

# Create your models here.

from django.core.validators import MinValueValidator
from django.db import models

from GardeningCareServicesApp.accounts.models import ServiceProviderProfile, HomeOwnerProfile
from GardeningCareServicesApp.services.validators import FileSizeValidator


# Create your models here.

class Service(models.Model):
    photo = models.ImageField(
        upload_to='',
        validators=[
            FileSizeValidator(1),
        ],
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=255,
    )

    description = models.TextField()

    category = models.ForeignKey(
        to='ServiceCategory',
        on_delete=models.CASCADE,
        related_name='category_services'
    )

    provider = models.ForeignKey(
        to=ServiceProviderProfile,
        on_delete=models.CASCADE,
        related_name='provider_services'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ],
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.name} by {self.provider}"


class ServiceCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='service_reviews',
    )

    # only homeowners can post comments
    user = models.ForeignKey(
        to=HomeOwnerProfile,
        on_delete=models.CASCADE,
        related_name='homeowner_reviews',

    )

    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
    )  # 1 to 5 stars

    comment = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.rating} stars for {self.service} by {self.user}"

    class Meta:
        # ensures only one review per user
        unique_together = ('service', 'user')

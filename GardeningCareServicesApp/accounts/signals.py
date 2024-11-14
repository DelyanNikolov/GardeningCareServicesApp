from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from GardeningCareServicesApp.accounts.models.app_profiles import ServiceProviderProfile, HomeOwnerProfile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Check the user_type to determine which profile to create
        if instance.user_type == 'Homeowner':
            HomeOwnerProfile.objects.create(user=instance)
        elif instance.user_type == 'Service Provider':
            ServiceProviderProfile.objects.create(user=instance)

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from GardeningCareServicesApp.accounts.models.app_profiles import ServiceProviderProfile, HomeOwnerProfile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    """
        Connects the associated AppUser with a Homeowner or Service Provider Profile.
    """
    if created:
        # Check the user_type to determine which profile to create
        if instance.user_type == 'Homeowner':
            HomeOwnerProfile.objects.create(user=instance)
        elif instance.user_type == 'Service Provider':
            ServiceProviderProfile.objects.create(user=instance)


@receiver(post_delete, sender=HomeOwnerProfile)
def disable_user_on_homeowner_deletion(sender, instance, **kwargs):
    """
    Disable the associated AppUser when a HomeOwnerProfile is deleted.
    """
    user = instance.user
    if user:
        user.is_active = False
        user.save()


@receiver(post_delete, sender=ServiceProviderProfile)
def disable_user_on_serviceprovider_deletion(sender, instance, **kwargs):
    """
    Disable the associated AppUser when a ServiceProviderProfile is deleted.
    """
    user = instance.user
    if user:
        user.is_active = False
        user.save()

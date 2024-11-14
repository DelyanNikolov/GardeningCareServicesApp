from django.db import models


class UserTypeChoices(models.TextChoices):
    HOMEOWNER = 'Homeowner', 'Homeowner'
    SERVICE_PROVIDER = 'Service Provider', 'Service Provider'

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GardeningCareServicesApp.accounts'

    def ready(self):
        import GardeningCareServicesApp.accounts.signals

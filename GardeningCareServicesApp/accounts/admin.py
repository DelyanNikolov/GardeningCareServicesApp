from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from GardeningCareServicesApp.accounts.forms import AppUserCreationForm, AppUserChangeForm
from GardeningCareServicesApp.accounts.models.app_profiles import HomeOwnerProfile, ServiceProviderProfile

# Register your models here.


UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(UserAdmin):
    model = UserModel
    add_form = AppUserCreationForm
    form = AppUserChangeForm

    list_display = ('pk', 'email', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('pk',)

    fieldsets = (
        ('Credentials', {'fields': ('email', 'password', )}),
        ('User type', {'fields': ('user_type',)}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "user_type"),
            },
        ),
    )


@admin.register(HomeOwnerProfile)
class HomeOwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone_number',)
    search_fields = ('user__email', 'address')


@admin.register(ServiceProviderProfile)
class ServiceProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'rating', 'years_of_experience')
    search_fields = ('user__email', 'business_name')

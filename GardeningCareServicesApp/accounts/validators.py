from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class PhoneNumberValidator:
    """Validates phone numbers. To contain only digits spaces and dashes"""
    def __init__(self, message=None):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = 'Please enter a valid phone number.'
        else:
            self.__message = value

    def __call__(self, value):
        allowed_chars = set('0123456789 +-')

        for char in value:
            if char not in allowed_chars:
                raise ValidationError(self.message)

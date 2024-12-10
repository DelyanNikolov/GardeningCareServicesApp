from unittest import TestCase

from django.core.exceptions import ValidationError


from GardeningCareServicesApp.accounts.validators import PhoneNumberValidator


class PhoneNumberValidatorTest(TestCase):
    def setUp(self):
        self.validator = PhoneNumberValidator()

    def test_default_message(self):
        # Check that the default message is set correctly
        self.assertEqual(self.validator.message, 'Please enter a valid phone number.')

    def test_custom_message(self):
        # Create a validator with a custom message
        custom_message = "Invalid phone number format!"
        validator = PhoneNumberValidator(message=custom_message)

        # Check that the custom message is used
        self.assertEqual(validator.message, custom_message)

    def test_valid_phone_number_expect_success(self):
        # Valid phone numbers (should pass validation)
        valid_numbers = [
            '1234567890',
            '123 456 7890',
            '+123-456-7890',
            '123+456 7890',
            '123-456 7890',
        ]

        for number in valid_numbers:
            try:
                self.validator(number)
            except ValidationError as e:
                self.fail(f"Validation failed for valid phone number {number}: {e}")

    def test_invalid_phone_number_expect_validation_error(self):
        # Invalid phone numbers (should raise a ValidationError)
        invalid_numbers = [
            '1234567890@',
            'abc1234567890',
            '12345#67890',
            '12 34 56 7890!',
            '12345^67890',
        ]

        for number in invalid_numbers:
            with self.assertRaises(ValidationError):
                self.validator(number)

import re

from django.core.exceptions import BadRequest
from rest_framework import serializers

from workbook.constants import *
from workbook.models.models import *


class SignUpSerializer(serializers.ModelSerializer):
    # choiceField returns default error message, and it does not allow you to easily customize the error message.
    # CharField it does not have a predefined validation.
    role = serializers.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'role']

    # Serializer Validation/ Field-level validation
    def validate_first_name(self, value):
        if len(value) < MINIMUM_NAME_LENGTH:
            raise serializers.ValidationError(f"Name must be at least {MINIMUM_NAME_LENGTH} characters long.")
        return value

    def validate_last_name(self, value):
        if len(value) < MINIMUM_NAME_LENGTH:
            raise serializers.ValidationError(f"Name must be at least {MINIMUM_NAME_LENGTH} characters long.")
        return value

    def validate_email(self, value):
        is_valid = re.match(EMAIL_PATTERN, value)

        if not is_valid:
            raise serializers.ValidationError("Check your email.")

        return value

    def validate_password(self, value):
        is_valid = re.match(PASSWORD_PATTERN, value)

        if not is_valid:
            raise serializers.ValidationError(
                f"Password must be more than {PASSWORD_MIN_LENGTH} characters long and contain both numeric and "
                "alphabetic characters."
            )

        return value

    def validate_role(self, value):
        if value not in [role.value for role in UserType]:
            raise serializers.ValidationError("Role must be either customer or worker.")
        return value

    def is_valid_raise(self, raise_exception=True):
        if not self.is_valid():
            if raise_exception:
                raise BadRequest(self.errors)

            return False

        return True


class SignUpResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role']

import re

from django.core.exceptions import BadRequest
from rest_framework import serializers
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
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value

    def validate_last_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value

    def validate_email(self, value):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = re.match(pattern, value)

        if not is_valid:
            raise serializers.ValidationError("Check your email.")

        return value

    def validate_password(self, value):
        pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{9,}$'
        is_valid = re.match(pattern, value)

        if not is_valid:
            raise serializers.ValidationError(
                "Password must be more than 8 characters long and contain both numeric and alphabetic characters."
            )

        return value

    def validate_role(self, value):
        if value not in [role.value for role in UserType]:
            raise serializers.ValidationError("Role must be either CUSTOMER or WORKER.")
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

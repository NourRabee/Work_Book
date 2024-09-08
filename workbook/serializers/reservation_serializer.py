from datetime import timedelta

from django.core.exceptions import BadRequest
from rest_framework import serializers

from workbook.models.models import *
from workbook.serializers.customer_serializer import CustomerSkillSerializer


class CustomerReservationResponseSerializer(serializers.ModelSerializer):
    worker_first_name = serializers.CharField(source='worker_skill.worker.user.first_name', read_only=True)
    worker_last_name = serializers.CharField(source='worker_skill.worker.user.last_name', read_only=True)
    skill = CustomerSkillSerializer(source='worker_skill.skill', read_only=True)
    start_date_time = serializers.CharField(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'worker_first_name',
            'worker_last_name',
            'start_date_time',
            'status',
            'skill'
        ]


class CreateReservationSerializer(serializers.Serializer):
    worker_skill_id = serializers.IntegerField(required=False)
    start_date_time = serializers.DateTimeField(required=False, default=None)
    reserved_time_in_seconds = serializers.IntegerField(required=False, default=None)

    def validate(self, data):
        if not data.get('start_date_time') and not data.get('reserved_time_in_seconds'):
            raise serializers.ValidationError(
                "At least one of 'start_date_time' or 'reserved_time_in_seconds' must be provided.")
        return data

    def validate_start_date_time(self, date):
        current_time = timezone.now()
        tomorrow = (current_time + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        if date and date < tomorrow:
            raise serializers.ValidationError("Start date must be at least tomorrow.")

        return date

    def validate_reserved_time_in_seconds(self, time):
        if time and time <= 0:
            raise serializers.ValidationError("Reserved time must be positive.")
        return time

    def is_valid_raise(self, raise_exception=True):
        if not self.is_valid():
            if raise_exception:
                raise BadRequest(self.errors)
            return False
        return True


class WorkerReservationResponseSerializer(serializers.ModelSerializer):
    customer_first_name = serializers.CharField(source='customer.user.first_name', read_only=True)
    customer_last_name = serializers.CharField(source='customer.user.last_name', read_only=True)
    skill = CustomerSkillSerializer(source='worker_skill.skill', read_only=True)
    start_date_time = serializers.CharField(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'customer_first_name',
            'customer_last_name',
            'start_date_time',
            'status',
            'skill'
        ]


class UpdateReservationByWorkerSerializer(serializers.Serializer):
    status = serializers.CharField()

    def validate_status(self, status):
        if status not in [status.value for status in ReservationStatus]:
            raise serializers.ValidationError(
                f"Invalid status. Allowed values are: {[status.value for status in ReservationStatus]}")
        return status

    def is_valid_raise(self, raise_exception=True):
        if not self.is_valid():
            if raise_exception:
                raise BadRequest(self.errors)
            return False
        return True

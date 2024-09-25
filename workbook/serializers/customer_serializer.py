from django.core.exceptions import BadRequest
from rest_framework import serializers

from workbook.models.models import *
from workbook.serializers.common_serializer import UserSerializer
from workbook.serializers.review_serializer import ReviewSerializer


class CustomerSerializer(serializers.Serializer):
    # profile_picture = serializers.ImageField()
    profile_picture = serializers.CharField()
    biography = serializers.CharField(max_length=300)

    def validate_biography(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Biography cannot be empty.")
        if len(value) > 300:
            raise serializers.ValidationError("Biography cannot exceed 300 characters.")
        return value

    def is_valid_raise(self, raise_exception=True):
        if not self.is_valid():
            if raise_exception:
                raise BadRequest(self.errors)
            return False
        return True


class CustomerUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'user']


class CustomerSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name', 'description']


class CustomerReservationSerializer(serializers.ModelSerializer):
    worker_first_name = serializers.CharField(source='worker_skill.worker.user.first_name', read_only=True)
    worker_last_name = serializers.CharField(source='worker_skill.worker.user.last_name', read_only=True)
    skill = CustomerSkillSerializer(source='worker_skill.skill', read_only=True)
    review = ReviewSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'worker_first_name',
            'worker_last_name',
            'start_date_time',
            'status',
            'skill',
            'review'
        ]


class CustomerDetailsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    # profile_picture = serializers.CharField()
    biography = serializers.CharField(source='user.biography')
    reservations = CustomerReservationSerializer(source='prefetched_reservations', many=True, read_only=True)

    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'email',
            # 'profile_picture',
            'biography',
            'reservations'
        ]

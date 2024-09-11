from django.core.exceptions import BadRequest
from rest_framework import serializers

from workbook.models.models import *
from workbook.serializers.common_serializer import UserSerializer, ReviewSerializer


class CustomerSerializer(serializers.Serializer):
    profile_picture = serializers.ImageField()
    biography = serializers.CharField(max_length=300)

    def validate_profile_picture(self, value):
        if not value.name.endswith(('jpg', 'jpeg', 'png')):
            raise serializers.ValidationError("Only JPG, JPEG, and PNG files are allowed.")
        if value.size > 2 * 1024 * 1024:  # 2MB limit
            raise serializers.ValidationError("Image size should be under 2MB.")
        return value

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
    reviews = ReviewSerializer(many=True, source='review_set', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'worker_first_name',
            'worker_last_name',
            'start_date_time',
            'status',
            'skill',
            'reviews'
        ]


class CustomerDetailsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    profile_picture = serializers.ImageField(source='user.profile_picture')
    biography = serializers.CharField(source='user.biography')
    reservations = CustomerReservationSerializer(source='reservation_set', many=True, read_only=True)

    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'email',
            'profile_picture',
            'biography',
            'reservations'
        ]


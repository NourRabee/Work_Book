from django.core.exceptions import BadRequest
from rest_framework import serializers

from workbook.models.models import *
from workbook.serializers.common_serializer import UserSerializer
from workbook.serializers.review_serializer import ReviewSerializer


class WorkerSerializer(serializers.Serializer):
    profile_picture = serializers.CharField()
    biography = serializers.CharField(max_length=300)
    job_title = serializers.CharField(max_length=50)
    day_start_time = serializers.IntegerField()
    day_end_time = serializers.IntegerField()

    def validate_biography(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Biography cannot be empty.")
        if len(value) > 300:
            raise serializers.ValidationError("Biography cannot exceed 300 characters.")
        return value

    def validate_job_title(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Job title cannot be empty.")
        if len(value) > 50:
            raise serializers.ValidationError("Job title cannot exceed 50 characters.")
        return value

    def validate_day_start_time(self, value):
        #  day_start_time must be between 0 (00:00) and 86399 (23:59:59)
        if value < 0 or value > 86399:
            raise serializers.ValidationError("Start time must be between 0 and 86399 seconds (00:00 to 23:59:59).")
        return value

    def validate_day_end_time(self, value):
        if value < 0 or value > 86399:
            raise serializers.ValidationError("End time must be between 0 and 86399 seconds (00:00 to 23:59:59).")
        return value

    def validate(self, data):
        day_start_time = data.get('day_start_time')
        day_end_time = data.get('day_end_time')

        # Check if day_start_time is before day_end_time
        if day_start_time is not None and day_end_time is not None:
            if day_end_time <= day_start_time:
                raise serializers.ValidationError("End time must be after start time.")

        return data

    def is_valid_raise(self, raise_exception=True):
        if not self.is_valid():
            if raise_exception:
                raise BadRequest(self.errors)
            return False
        return True


class WorkerReservationSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(read_only=True)
    customer_first_name = serializers.CharField(source='customer.user.first_name', read_only=True)
    customer_last_name = serializers.CharField(source='customer.user.last_name', read_only=True)

    class Meta:
        model = Reservation
        fields = ['customer_first_name', 'customer_last_name', 'start_date_time', 'status', 'review']


class WorkerSkillSerializer(serializers.ModelSerializer):
    reservations = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = ['name', 'description', 'reservations']

    def get_reservations(self, worker):
        worker_skill = self.context.get('worker_skill')
        reservations = worker_skill.prefetched_reservations
        return WorkerReservationSerializer(reservations, many=True).data


class WorkerDetailsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    # profile_picture = serializers.CharField()
    biography = serializers.CharField(source='user.biography')
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        fields = [
            'first_name',
            'last_name',
            'email',
            # 'profile_picture',
            'biography',
            'job_title',
            'day_start_time',
            'day_end_time',
            'skills'
        ]

    def get_skills(self, worker):
        worker_skills = worker.prefetched_skills
        skills_data = []
        for worker_skill in worker_skills:
            skill_serializer = WorkerSkillSerializer(worker_skill.skill, context={'worker_skill': worker_skill})
            skills_data.append(skill_serializer.data)
        return skills_data


class WorkerUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Worker
        fields = ['id', 'job_title', 'day_start_time', 'day_end_time', 'user']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description']

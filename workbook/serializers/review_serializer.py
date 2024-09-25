from django.core.exceptions import BadRequest, ValidationError
from rest_framework import serializers
from workbook.models.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['stars', 'description']

    def validate_stars(self, stars):
        if not (1 <= stars <= 5):
            raise ValidationError("Stars must be an integer between 1 and 5.")
        return stars

    def is_valid_raise(self, raise_exception=True):
        if not self.is_valid():
            if raise_exception:
                raise BadRequest(self.errors)
            return False
        return True


class GetCustomerReviewSerializer(serializers.ModelSerializer):
    skill = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['stars', 'description', 'skill']

    def get_skill(self, review):
        try:
            skill = review.reservation.worker_skill.skill
            return skill.name
        except AttributeError:
            return None

    def validate_stars(self, stars):
        if not (1 <= stars <= 5):
            raise serializers.ValidationError("Stars must be an integer between 1 and 5.")
        return stars


class GetWorkerReviewsSerializer(serializers.ModelSerializer):
    skill = serializers.SerializerMethodField()
    customer_first_name = serializers.SerializerMethodField()
    customer_last_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['stars', 'description', 'skill', 'customer_first_name', 'customer_last_name']

    def get_skill(self, review):
        try:
            skill = review.reservation.worker_skill.skill
            return skill.name
        except AttributeError:
            return None

    def get_customer_first_name(self, review):
        try:
            customer = review.reservation.customer
            return customer.user.first_name
        except AttributeError:
            return None

    def get_customer_last_name(self, review):
        try:
            customer = review.reservation.customer
            return customer.user.last_name
        except AttributeError:
            return None

    def validate_stars(self, stars):
        if not (1 <= stars <= 5):
            raise serializers.ValidationError("Stars must be an integer between 1 and 5.")
        return stars

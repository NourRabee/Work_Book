from workbook.models.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_picture', 'biography']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['stars', 'description']

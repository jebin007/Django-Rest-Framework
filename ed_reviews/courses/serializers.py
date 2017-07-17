from rest_framework import serializers
from . import models

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'email': {'write_only': True}
        }
        model = models.Review
        fields = (
            'id',
            'course',
            'name',
            'email',
            'comment',
            'rating',
            'created_at',
        )

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = (
            'id',
            'title',
            'url',
            )
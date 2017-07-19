from rest_framework import serializers
from . import models
from django.db.models import Avg

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

    def validate_rating(self, value):
        if value in range(1, 6):
            return value
        raise serializers.ValidationError(
            'Rating must be an integer between 1 and 5'
        )

class CourseSerializer(serializers.ModelSerializer):
    reviews = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='apiv2:review-detail')
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = models.Course
        fields = (
            'id',
            'title',
            'url',
            'reviews',
            'average_rating',
            )

    def get_average_rating(self, obj):  # get_fieldname which in this case is average_rating
        average = obj.reviews.aggregate(Avg('rating')).get('rating__avg')

        if average is None:
            return 0
        return round(average * 2) / 2

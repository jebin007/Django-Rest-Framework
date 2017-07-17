from rest_framework import generics
from django.shortcuts import get_object_or_404

from . import models
from . import serializers
# Create your views here.

class ListCreateCourse(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

class RetrieveUpdateDestroyCourse(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

class ListCreateReview(generics.ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return self.queryset.filter(course_id=self.kwargs.get('course_pk'))
    #this method overriders the queryset from objects.all to a more specific one.

    def perform_create(self, serializer):
        course = get_object_or_404(models.Course, pk=self.kwargs.get('course_pk'))
        serializer.save(course=course)
    #this method prevents a user from being able to give a different pk when they submit that.

class RetrieveUpdateDestroyReview(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            course_id=self.kwargs.get('course_pk'),
            pk=self.kwargs.get('pk')
        )
    #get queryset gets multiple items whereas get_objects gets single item.
    #out of this queryset get a single object that has this course id and this pk.
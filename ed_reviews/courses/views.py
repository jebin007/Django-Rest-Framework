from rest_framework import generics
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import permissions

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

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            if request.method == 'DELETE':
                return False


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsSuperUser,
        permissions.DjangoModelPermissions,
    )  #For this viewset, ignore default permissions and care about Django Model Permissions
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

    @detail_route(methods=['get'])
    def reviews(self, request, pk=None):
        self.pagination_class.page_size = 5
        reviews = models.Review.objects.filter(course=pk)   #get all the reviews for current course
        page = self.paginate_queryset(reviews)

        if page is not None:
            serializer = serializers.ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

        course = self.get_object()
        serializer = serializers.ReviewSerializer(course.reviews.all(), many=True)
        return Response(serializer.data)
    #This method makes the url for /api/v2/courses/1(x)/reviews and is called adhoc method
    #By doing this the reivews are list view only, users cannot create new reviews.

class ReviewViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   #mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

#the mixins inherited in this class, helps us to remove the list view for all reviews located in
# localhost:8000/api/v2/reviews/ as it doesn't make sense to show all reviews.
#However, if we navigate to a single review eg: api/v2/reviews/1 it still works.
#the only thing I had to do to remove the list view for all reviews was to import mixins and remove ListModeMixin
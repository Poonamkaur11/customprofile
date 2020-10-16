from datetime import datetime
from time import timezone

import django_filters

import rest_framework.mixins as mixin
from django_filters import DateFilter, DateRangeFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django.core.mail import send_mail
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

from users.models import User, Profile, Education, Experience, Feed, Skills
from users.serializers import UserSerializer, ProfileSerializer, EducationSerializer, ExperienceSerializer, \
    FeedSerializer, SkillsSerializer
from .Base_views import BaseViewSet
from rest_framework import (viewsets, filters)
from filters.mixins import (
    FiltersMixin,
)
from url_filter.integrations.drf import DjangoFilterBackend


def mail(request):
    # return HttpResponse(request.GET)
    subject = "Welcome"
    msg = "Congratulations for your success"
    to = "poonamkaur1108@gmail.com"
    res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
    if res == 1:
        msg = "Mail Sent"
    else:
        msg = "Mail could not sent"
    return HttpResponse(request.GET)


class TwoItemsSetPagination(PageNumberPagination):
    page_size = 2


class UserViewSet(BaseViewSet):
    model_class = User
    pagination_class = TwoItemsSetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    head = "user"
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, ]
    search_fields = ('name', 'email', 'Profile__gender', 'created_at')
    filter_fields = ('name', 'email', 'Profile__gender')


class ProfileFilter(DjangoFilterBackend):
    class Meta:
        model = Profile
        fields = ['bio', 'city']


class ProfileViewSet(BaseViewSet):
    pagination_class = TwoItemsSetPagination

    ordering_fields = ('user', 'bio')

    head = "profile"

    filter_backends = [filters.SearchFilter, DjangoFilterBackend, ]
    filter_fields = ('bio', 'city', 'created_at')
    search_fields = ('bio', 'city', 'created_at')
    queryset = Profile.objects.all()
    model_class = Profile
    serializer_class = ProfileSerializer


class EducationViewSet(BaseViewSet):
    model_class = Education
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, OrderingFilter]
    filter_fields = ('university', 'degree', 'created_at', 'start_date', 'end_date')
    search_fields = ('university', 'degree')

    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    pagination_class = TwoItemsSetPagination
    ordering_fields = "__all__"
    head = "education"


class ExperienceViewSet(BaseViewSet):
    model_class = Experience
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_fields = ('title', 'company', 'created_at', 'start_date', 'end_date')
    search_fields = ('title', 'company')
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    pagination_class = TwoItemsSetPagination
    head = "experience"


class FeedViewSet(BaseViewSet):
    model_class = Feed
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    pagination_class = TwoItemsSetPagination
    filter_fields = ('created_at', 'feed')
    search_fields = ('feed', 'created_at')
    head = "feed"


#    def list(self, request, **kwargs):
#        fed = Feed.objects.all()
#        page = self.paginate_queryset(fed)
#        if page is not None:
#            serializer = self.get_paginated_response(self.serializer_class(page,
#                                                                           many = True).data)
#        else:
#            serializer = FeedSerializer(fed, many = True)
#        return Response({"status": "true", "message": "data listed successfully.", "data": serializer.data})


class SkillsViewSet(BaseViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.

      """

    model_class = Skills
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_fields = ('skills', 'created_at')
    search_fields = ('skills', 'created_at')
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    pagination_class = TwoItemsSetPagination
    head = "Skills"

from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from users.pagination import PaginationHandlerMixin
from users.models import User, Profile, Education, Experience, Feed, Skills
from users.serializers import UserSerializer, ProfileSerializer, EducationSerializer, ExperienceSerializer, \
    FeedSerializer, SkillsSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .Base_views import BaseViewSet
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets


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


class ProfileViewSet(BaseViewSet):
    pagination_class = TwoItemsSetPagination
    queryset = Profile.objects.all()
    model_class = Profile
    serializer_class = ProfileSerializer
    head = "profile"


class EducationViewSet(BaseViewSet):
    model_class = Education
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    pagination_class = TwoItemsSetPagination
    head = "education"


class ExperienceViewSet(BaseViewSet):
    model_class = Experience
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    pagination_class = TwoItemsSetPagination
    head = "experience"


class FeedViewSet(BaseViewSet):
    model_class = Feed

    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    pagination_class = TwoItemsSetPagination
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

    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    pagination_class = TwoItemsSetPagination
    head = "Skills"

from django.shortcuts import render, redirect
from rest_framework import generics
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
from .Base_views import BaseDetails
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination


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


class UserList(generics.ListCreateAPIView):
    pagination_class = TwoItemsSetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = UserSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"status": "true", "message": "data Posted successfully.", "data": {"uuid": serializer.data['uuid']}},
                status = status.HTTP_201_CREATED)
        return Response({'message': 'user with this email already exist', }, status = status.HTTP_400_BAD_REQUEST)

    def get(self, request, **kwargs):
        user = User.objects.all()
        page = self.paginate_queryset(user)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many = True).data)
        else:
            serializer = ProfileSerializer(user, many = True)

        return Response({"status": "true", "message": "data Retrieve successfully.", "data": serializer.data})


class UserDetail(BaseDetails):
    model_class = User
    serializer_class = UserSerializer

    head = "user"


class ProfileDetail(BaseDetails):
    model_class = Profile
    serializer_class = ProfileSerializer
    head = "profile"


class ProfileList(generics.ListCreateAPIView):
    pagination_class = TwoItemsSetPagination
    queryset = Profile.objects.all()

    serializer_class = ProfileSerializer

    def get(self, request, **kwargs):
        profile = Profile.objects.all()
        page = self.paginate_queryset(profile)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many = True).data)
        else:
            serializer = ProfileSerializer(profile, many = True)

        return Response({"status": "true", "message": "data Retrieve successfully.", "data": serializer.data})


class EducationDetail(BaseDetails):
    model_class = Education
    serializer_class = EducationSerializer

    head = "education"


class EducationList(generics.ListCreateAPIView):
    pagination_class = TwoItemsSetPagination
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def get(self, request, **kwargs):
        education = Education.objects.all()
        page = self.paginate_queryset(education)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many = True).data)
        else:

            serializer = EducationSerializer(education, many = True)
        return Response({"status": "true", "message": "data Retrieve successfully.", "data": serializer.data})


class ExperienceDetail(BaseDetails):
    model_class = Experience
    serializer_class = ExperienceSerializer
    head = "experience"


class ExperienceList(generics.ListCreateAPIView):
    pagination_class = TwoItemsSetPagination
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

    def get(self, request, **kwargs):
        experience = Experience.objects.all()
        page = self.paginate_queryset(experience)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many = True).data)
        else:
            serializer = ExperienceSerializer(experience, many = True)
        return Response({"status": "true", "message": "data Retrieve successfully.", "data": serializer.data})


class FeedList(generics.RetrieveUpdateDestroyAPIView):
    pagination_class = TwoItemsSetPagination
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    def get(self, request, **kwargs):
        fed = Feed.objects.all()
        page = self.paginate_queryset(fed)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many = True).data)
        else:
            serializer = FeedSerializer(fed, many = True)
        return Response({"status": "true", "message": "data Retrieve successfully.", "data": serializer.data})


class FeedDetail(BaseDetails):
    model_class = Feed
    serializer_class = FeedSerializer
    head = "feed"


class SkillsList(generics.RetrieveUpdateDestroyAPIView):
    pagination_class = TwoItemsSetPagination
    queryset = Skills.objects.all()
    serializer_class = FeedSerializer

    def get(self, request, **kwargs):
        skill = Skills.objects.all()
        page = self.paginate_queryset(skill)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many = True).data)
        else:
            serializer = SkillsSerializer(skill, many = True)
        return Response({"status": "true", "message": "data Retrieve successfully.", "data": serializer.data})


class SkillsDetail(BaseDetails):
    model_class = Skills
    serializer_class = SkillsSerializer
    head = "skill"

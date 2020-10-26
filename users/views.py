import uuid
from datetime import datetime
from time import timezone

from django.conf import settings
from requests import Response
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView, \
    DestroyAPIView, GenericAPIView, RetrieveAPIView

import django_filters
from django.http import HttpResponse, request
import rest_framework.mixins as mixin
from django_filters import DateFilter, DateRangeFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django.core.mail import send_mail
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from self import self

from users.models import User, Profile, Education, Experience, Feed, Skills, FollowRequest
from users.serializers import UserSerializer, ProfileSerializer, EducationSerializer, ExperienceSerializer, \
    FeedSerializer, SkillsSerializer, FollowRequestSerializer, UserProfileSerializer
from . import models
from .Base_views import BaseViewSet
from rest_framework import (viewsets, filters, status)
from filters.mixins import (
    FiltersMixin,
)
from url_filter.integrations.drf import DjangoFilterBackend


def follow(request, username):
    pass


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
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ('name', 'email', 'created_at')
    filter_fields = ('name', 'email',)
    ordering_fields = "__all__"



class ProfileFilter(DjangoFilterBackend):
    class Meta:
        model = Profile
        fields = ['bio', 'city']


class ProfileViewSet(BaseViewSet):
    pagination_class = TwoItemsSetPagination

    ordering_fields = ('user', 'bio')

    head = "profile"

    filter_backends = [filters.SearchFilter, DjangoFilterBackend, OrderingFilter]
    filter_fields = ('bio', 'city', 'created_at')
    search_fields = ('bio', 'city', 'created_at')
    ordering_fields = "__all__"
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
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, OrderingFilter]
    filter_fields = ('title', 'company', 'created_at', 'start_date', 'end_date')
    search_fields = ('title', 'company')
    ordering_fields = "__all__"
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    pagination_class = TwoItemsSetPagination
    head = "experience"


class FeedViewSet(BaseViewSet):
    model_class = Feed
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, OrderingFilter]
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    pagination_class = TwoItemsSetPagination
    filter_fields = ('created_at', 'feed')
    search_fields = ('feed', 'created_at')
    ordering_fields = "__all__"
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
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, OrderingFilter]
    filter_fields = ('skills', 'created_at')
    search_fields = ('skills', 'created_at')
    ordering_fields = "__all__"
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    pagination_class = TwoItemsSetPagination
    head = "Skills"


'''class FollowRequestViewSet(viewsets.ViewSet):
    queryset = User.objects.all

    def follow(self, request, pk):
        own_profile = request.user.profile_set.first()  # or your queryset to get
        following_profile = Profile.objects.get(id=pk)
        own_profile.following.add(following_profile)  # and .remove() for unfollow
        return Response({'message': 'now you are following'}, status=status.HTTP_200_OK)

    def unfollow(self, request, pk):
        own_profile = request.user.profile_set.first()  # or your queryset to get
        following_profile = Profile.objects.get(id=pk)
        own_profile.following.remove(following_profile)  # and .remove() for unfollow
        return Response({'message': 'you are no longer following him'}, status=status.HTTP_200_OK)'''

# POST: follow a user


class Follow(UpdateAPIView):
    serializer_class = UserSerializer
    lookup_url_kwarg = "user_id"

    def patch(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        User.objects.__getattribute__(uuid=user_id).followed_by.add(self.request.user.user_profile)
        return Response(f"{self.email} follows {User.objects.__getattribute__(uuid=user_id).email}")


# POST: unfollow a user
class Unfollow(DestroyAPIView):
    queryset = ProfileSerializer
    serializer_class = ProfileSerializer
    lookup_url_kwarg = "user_id"

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        to_delete = User.objects.get(uuid=user_id)
        self.request.user.user_profile.follow.remove(to_delete)
        return Response("Unfollowed!")


# GET: List of all the followers
class ListFollowers(ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        followers_profile = self.request.user.followed_by.all()
        return [up.user for up in followers_profile]


# GET: List of all the people the user is following
class ListFollowing(ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        following_profiles = self.request.user.user_profile.follow.all()
        return following_profiles


class SendFollowRequest(CreateAPIView):
    serializer_class = FollowRequestSerializer
    lookup_url_kwarg = "user_id"

    def create(self, request, *args, **kwargs):
        receiver_id = kwargs["user_id"]
        receiver = User.objects.get(uuid=receiver_id)
        if self.request.user.uuid != receiver.uuid:
            FollowRequest.objects.create(sender=self.request.user, receiver=receiver)
            return Response(f"{self.request.user.uuid} sent a follow request to {receiver.uuid}")
        return Response(f"You can't send a follow request to yourself, {self.request.user.uuid}")


class AcceptFollowRequest(CreateAPIView):
    serializer_class = FollowRequestSerializer
    lookup_url_kwarg = "user_id"

    def create(self, request, *args, **kwargs):
        sender_id = kwargs["request_id"]
        try:
            sender = User.objects.get(uuid=sender_id)
        except User.DoesNotExist:
            return Response(f"There is no user with ID {sender_id}")
        try:
            pending_request = FollowRequest.objects.get(receiver=self.request.user.uuid, sender=sender_id)
            FollowRequest.objects.get_or_create(sender=self.request.user, receiver=sender, status="friends")
            pending_request.status = "friends"
            pending_request.save()
            return Response(f"{self.request.user.uuid} and {sender.uuid} are now friends!")
        except FollowRequest.DoesNotExist:
            return Response(f"{sender.uuid} did not send you a follow request.")

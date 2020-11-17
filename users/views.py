import uuid
from datetime import datetime

from time import timezone
from django.core.mail import EmailMessage
from allauth.account.views import email
from django.conf import settings
from django.db.migrations import serializer
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from drf_multiple_model.views import ObjectMultipleModelAPIView
from requests import Response
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView, \
    DestroyAPIView, GenericAPIView, RetrieveAPIView
from rest_framework import permissions
import django_filters
from django.http import HttpResponse, request, Http404, response
import rest_framework.mixins as mixin
from django_filters import DateFilter, DateRangeFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.request import clone_request
from rest_framework.templatetags.rest_framework import data
from self import self

from users.models import User, Profile, Education, Experience, Feed, Skills, FriendRequest
from users.serializers import UserSerializer, ProfileSerializer, EducationSerializer, ExperienceSerializer, \
    FeedSerializer, SkillsSerializer, FriendRequestSerializer, UserProfileSerializer, UserRequestSerializer
from . import models
from .Base_views import BaseViewSet
from rest_framework import (viewsets, filters, status)
from filters.mixins import (
    FiltersMixin,
)
from url_filter.integrations.drf import DjangoFilterBackend
import logging

logger = logging.getLogger('django')
logging.basicConfig(level=logging.INFO, format='%(asctime)s ::%(levelname)s ::%(message)s')

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    head = "user"
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ('name', 'email', 'created_at')
    filter_fields = ('name', 'email',)
    ordering_fields = "__all__"
    logger.info('Users')


class ProfileViewSet(BaseViewSet):
    pagination_class = TwoItemsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    ordering_fields = ('user', 'bio')

    head = "profile"

    filter_backends = [filters.SearchFilter, DjangoFilterBackend, OrderingFilter]
    filter_fields = ('bio', 'city', 'created_at')
    search_fields = ('bio', 'city', 'created_at')
    ordering_fields = "__all__"
    queryset = Profile.objects.all()
    model_class = Profile
    serializer_class = ProfileSerializer
    logger.info('Profile')


class EducationViewSet(BaseViewSet):
    model_class = Education
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, OrderingFilter]
    filter_fields = ('university', 'degree', 'created_at', 'start_date', 'end_date')
    search_fields = ('university', 'degree')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    pagination_class = TwoItemsSetPagination
    ordering_fields = "__all__"
    head = "education"
    logger.info('Education')


class ExperienceViewSet(BaseViewSet):
    model_class = Experience
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, OrderingFilter]
    filter_fields = ('title', 'company', 'created_at', 'start_date', 'end_date')
    search_fields = ('title', 'company')
    ordering_fields = "__all__"
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    pagination_class = TwoItemsSetPagination
    head = "experience"
    logger.info('Experience')


class FeedViewSet(BaseViewSet):
    model_class = Feed
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, OrderingFilter]
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    pagination_class = TwoItemsSetPagination
    filter_fields = ('created_at', 'feed')
    search_fields = ('feed', 'created_at')
    ordering_fields = "__all__"
    head = "feed"
    logger.info('Feed')


class SkillsViewSet(BaseViewSet):
    model_class = Skills
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, OrderingFilter]
    filter_fields = ('skills', 'created_at')
    search_fields = ('skills', 'created_at')
    ordering_fields = "__all__"
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    pagination_class = TwoItemsSetPagination
    head = "Skills"
    logger.info('Skills')


class Follow(UpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    lookup_url_kwarg = "user_id"

    def patch(self, request, *args, **kwargs):
        user_to_follow_id = self.kwargs.get("user_id")
        user_to_follow = User.objects.get(uuid=user_to_follow_id)

        if user_to_follow not in self.request.user.user_profile.follow.all():
            if user_to_follow.public is True:
                user_to_follow.followed_by.add(self.request.user.user_profile)
                sendmail = EmailMessage(
                    subject="New Follower",
                    body=f"Hi {user_to_follow.email}\n\n{self.request.user.email} is now following you!",
                    from_email="pkeb1190@gmail.com",
                    to=[f"{user_to_follow.email}"],
                )
                sendmail.send()
                return HttpResponse(f"{self.request.user.email} follows {user_to_follow.email}")
            else:
                return HttpResponse(f"{self.request.user.email} cannot follow private user {user_to_follow.email}")
        return HttpResponse(f"{self.request.user.email} is already following {user_to_follow.email}")


class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = 2


class FollowPrivate(ObjectMultipleModelAPIView):
    pagination_class = LimitPagination
    querylist = [
        {'queryset': User.objects.all(), 'serializer_class': UserSerializer},
        {'queryset': FriendRequest.objects.all(), 'serializer_class': FriendRequestSerializer},
        {'queryset': Profile.objects.all(), 'serializer_class': ProfileSerializer},
    ]

    lookup_url_kwarg = "user_id"

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        accepted_requests = self.request.user.received_friend_request.all().filter(status="friends")
        friends = [fr.sender for fr in accepted_requests]
        return friends

    def patch(self, request, *args, **kwargs):
        user_to_follow_id = self.kwargs.get("user_id")
        user_to_follow = User.objects.get(uuid=user_to_follow_id)
        if user_to_follow.received_friend_request.all().filter(status="friends"):
            user_to_follow.followed_by.add(self.request.user.user_profile)
            sendmail = EmailMessage(
                subject="New Follower",
                body=f"Hi {user_to_follow.email}\n\n{self.request.user.email} is now following you!",
                from_email="pkeb1190@gmail.com",
                to=[f"{user_to_follow.email}"],
            )
            sendmail.send()
            return HttpResponse(f"{self.request.user.email} follows {user_to_follow.email}")

        return HttpResponse(f"{self.request.user.email} is not friend to  {user_to_follow.email}")


class Unfollow(DestroyAPIView):
    queryset = ProfileSerializer
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = "user_id"

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        to_delete = User.objects.get(uuid=user_id)
        self.request.user.user_profile.follow.remove(to_delete)
        # return self.destroy(request, *args, **kwargs)
        return HttpResponse("Unfollowed!")


class ShowFriends(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        accepted_requests = self.request.user.received_friend_request.all().filter(status="friends")
        friends = [fr.sender for fr in accepted_requests]
        return friends

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "status": "true",
                "message": "data listed successfully.",
                "data": serializer.data
            }
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "true", "message": "data listed successfully.", "data": serializer.data})


# GET: List of all the followers
class ListFollowers(ListAPIView):
    serializer_class = UserProfileSerializer
    pagination_class = TwoItemsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        followers_profile = self.request.user.followed_by.all()
        return [up.user for up in followers_profile]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "status": "true",
                "message": "data listed successfully.",
                "data": serializer.data
            }
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "true", "message": "data listed successfully.", "data": serializer.data})


# GET: List of all the people the user is following
class ListFollowing(ListAPIView):
    serializer_class = UserProfileSerializer
    pagination_class = TwoItemsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        following_profiles = self.request.user.user_profile.follow.all()
        return following_profiles

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "status": "true",
                "message": "data listed successfully.",
                "data": serializer.data
            }
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "true", "message": "data listed successfully.", "data": serializer.data})


class SendFriendRequest(GenericAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    lookup_url_kwarg = "user_id"

    def post(self, request, *args, **kwargs):
        receiver_id = kwargs["user_id"]
        receiver = User.objects.get(uuid=receiver_id)
        if self.request.user.uuid != receiver.uuid:
            friend_request, created = FriendRequest.objects.get_or_create(sender=self.request.user, receiver=receiver)

            if created:
                sendmail = EmailMessage(
                    subject="New friend request",
                    body=f"Hi {receiver.email}\n\n{self.request.user.email} sent you a friend request!",
                    from_email="pkeb1190.com",
                    to=[f"{receiver.email}"],
                )
                sendmail.send()
                return HttpResponse(f"{self.request.user.email} sent a friend request to {receiver.email}")
            else:
                return HttpResponse(f"You have already sent a friend request to {receiver.email}")
        return HttpResponse(f"You can't send a friend request to yourself, {self.request.user.email}")


class ShowPendingSentFriendRequests(ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        sent_requests = FriendRequest.objects.filter(status="pending", sender_id=self.request.user.uuid)
        return sent_requests

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "status": "true",
                "message": "data listed successfully.",
                "data": serializer.data
            }
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "true", "message": "data listed successfully.", "data": serializer.data})


# GET: List all open friend requests from others
class ShowPendingReceivedFriendRequests(ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        received_requests = FriendRequest.objects.filter(status="pending", receiver_id=self.request.user.uuid)
        return received_requests

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "status": "true",
                "message": "data listed successfully.",
                "data": serializer.data
            }
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "true", "message": "data listed successfully.", "data": serializer.data})


# GET: List all my pending friend requests
class ShowPendingSentFriendRequests(ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        sent_requests = FriendRequest.objects.filter(status="pending", sender_id=self.request.user.uuid)
        return sent_requests

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "status": "true",
                "message": "data listed successfully.",
                "data": serializer.data
            }
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "true", "message": "data listed successfully.", "data": serializer.data})


class AcceptFriendRequest(GenericAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = "request_id"

    def post(self, request, *args, **kwargs):
        request_id = kwargs["request_id"]
        try:
            friend_request = FriendRequest.objects.get(uuid=request_id)
            sender = User.objects.get(uuid=friend_request.sender_id)
            receiver = User.objects.get(uuid=friend_request.receiver_id)
            if friend_request.status == "pending" and self.request.user.uuid == receiver.uuid:
                FriendRequest.objects.create(sender=receiver, receiver=sender, status="friends")
                friend_request.status = "friends"
                friend_request.save()
                sendmail = EmailMessage(
                    subject=f"You have a new friend!",
                    body=f"Hi {sender.email}\n\n{receiver.email} accepted your friend request!",
                    from_email="pkeb1190@gmail.com",
                    to=[f"{sender.email}"],
                )
                sendmail.send()
                return HttpResponse(f"{sender.email} and {receiver.email} are now friends!")
            elif friend_request.status == "friends" and self.request.user.uuid == receiver.uuid:
                return HttpResponse(f"{sender.email} and {receiver.email} are already friends!")
            else:
                return HttpResponse(f"{self.request.user.email} is not part of this friend request.")
        except FriendRequest.DoesNotExist:
            return HttpResponse(f"There is no friend request with ID {request_id}")

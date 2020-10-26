import profile

import django_filters
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_auth.tests import settings
from rest_framework import serializers, status
from rest_framework.response import Response

from users.models import Profile, Experience, Education, User, Feed, Skills, FollowRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = "__all__"


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ExperienceSerializer(serializers.ModelSerializer):
    # uuid = serializers.UUIDField(required = True, read_only = False)

    class Meta:
        model = Experience
        fields = "__all__"


class EducationSerializer(serializers.ModelSerializer):
    # uuid = serializers.UUIDField(required = True, read_only = False)

    class Meta:
        model = Education
        fields = "__all__"


'''class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = "__all__"


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = "__all__"'''


class FollowRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FollowRequest
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    user_profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ["email", "user_profile", "last_login"]

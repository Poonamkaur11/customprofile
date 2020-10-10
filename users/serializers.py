from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_auth.tests import settings
from rest_framework import serializers, status
from rest_framework.response import Response

from users.models import Profile, Experience, Education, User, Feed, Skills


class UserSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(required = True, read_only = False)

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


'''class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required = True)
    experience = ExperienceSerializer(required = True)
    education = EducationSerializer(required = True)
    feed = FeedSerializer(required = True)
    skills = SkillsSerializer(required = True)

    class Meta:
        model = User
        fields = '__all__'
        extra_fields = 'profile', 'experience', 'education', 'uuid', 'feed', 'skills'''

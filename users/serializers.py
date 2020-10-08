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

        def patch(self, request, uuid):

            serializer = ExperienceSerializer(exp, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "true", "message": "data updated successfully.", "data": serializer.data})
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        def delete(self, request, uuid):
            user = self.get_object(uuid)
            user.delete()
            return Response({"status": "true", "message": "data Deleted successfully.", },
                            status = status.HTTP_204_NO_CONTENT)

        def get(self, uuid):
            user = self.get_object(uuid)
            user.save()
            return Response({"status": "true", "message": "data retrieved successfully."},
                            status = status.HTTP_204_NO_CONTENT)


class EducationSerializer(serializers.ModelSerializer):
    # uuid = serializers.UUIDField(required = True, read_only = False)

    class Meta:
        model = Education
        fields = "__all__"
        extra_fields = 'uuid'

        def patch(self, request, uuid):
            self.get_object(uuid)
            serializer = ExperienceSerializer(user, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "true", "message": "data updated successfully.", "data": serializer.data})
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        def delete(self, request, uuid):
            self.get_object(uuid)
            user.delete()
            return Response({"status": "true", "message": "data Deleted successfully.", },
                            status = status.HTTP_204_NO_CONTENT)

        def get(self, uuid):
            self.get_object(uuid)
            user.save()
            return Response({"status": "true", "message": "data retrieved successfully."},
                            status = status.HTTP_204_NO_CONTENT)

        def get_object(self, uuid):
            pass


class UsersSerializer(serializers.ModelSerializer):

    def validated_password(self, value):
        return make_password(value)

    profile = ProfileSerializer(read_only = True, many=True)
    experience = ExperienceSerializer(read_only = True, many=True)
    education = EducationSerializer(read_only = True, many=True)
    feed = FeedSerializer(read_only = True, many=True)
    skills = SkillsSerializer(read_only = True, many=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_fields = 'profile', 'experience', 'education', 'uuid', 'feed', 'skills'

    def create(self, validated_data):
        user = User.objects.create(
            email = validated_data['email'],
        )
        profile_data = validated_data.pop('Profile')
        Profile.objects.create(
            user = User,
            profile_pic = Profile['profile_pic'],
            bio = Profile['bio'],
            headline = Profile['headline'],
        )

        Experience.objects.create(
            Experience = Experience['experience'],
        )
        Education.objects.create(
            highest_education = Education['highest_education'],
        )
        Feed.objects.create(
            feed = Feed['feed'],
        )
        Skills.objects.create(
                skills = Skills['skills'],
        )
        return user

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

    def post(self, request, uuid):
        user = self.get_object(uuid)
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "true", "message": "data updated successfully.", "data": serializer.data})
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        user = self.get_object(uuid)
        user.delete()
        return Response({"status": "true", "message": "data Deleted successfully.", },
                        status = status.HTTP_204_NO_CONTENT)

    def get(self, uuid):
        user = self.get_object(uuid)
        user.save()
        return Response({"status": "true", "message": "data retrieved successfully."},
                        status = status.HTTP_204_NO_CONTENT)

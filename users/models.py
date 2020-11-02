from datetime import timedelta
import django_filters
import jwt
import self as self
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django_filters import rest_framework as filters
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
# from datetime import datetime
# from django.utils.translation import ugettext_lazy as __
import uuid
# from django.conf import settings
from django.db.models.functions import datetime
from notifications.signals import notify
from hello_django import settings
from .managers import UserManager


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email_address", max_length=300, unique=True)
    name = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    spouse_name = models.CharField(blank=True, max_length=100)
    public = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    profile_pic = models.ImageField(default='None', upload_to='profile_pics', blank=True, null=True)
    bio = models.CharField(default=None, max_length=500, null=True)
    headline = models.CharField(default=None, max_length=100, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    country_code = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(verbose_name='date_of_birth', blank=True, default=None, null=True)
    follow = models.ManyToManyField(to=User, related_name="followed_by", )

    def __str__(self):
        return f'{self.user.email}'


class Education(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100, default=False)
    university = models.CharField(max_length=100, default=False)
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None)

    def __str__(self):
        return f'{self.user.email}'


class Experience(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.CharField(blank=True, max_length=100, default=False)
    title = models.CharField(max_length=100, default=False)
    project = models.TextField(max_length=200, default=False)
    company = models.CharField(max_length=200, default=False)
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None)

    def __str__(self):
        return f'{self.user.email}'


class Feed(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    feed = models.TextField(default=False)

    def __str__(self):
        return f'{self.user.email}'


class Skills(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.TextField(default=False)

    def __str__(self):
        return f'{self.user.email}'


class FriendRequest(BaseModel):
    PENDING = "pending"
    FRIENDS = "friends"
    status = models.CharField(
        verbose_name="status",
        max_length=100,
        choices=(
            (PENDING, PENDING),
            (FRIENDS, FRIENDS),
        ),
        default=PENDING
    )
    sender = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_friend_request"
    )
    receiver = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_friend_request"
    )

    def __str__(self):
        return f"{self.sender} sent friend request to {self.receiver}. Status: {self.status}"

from datetime import timedelta

import jwt
from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
# from datetime import datetime
# from django.utils.translation import ugettext_lazy as __
import uuid
# from django.conf import settings
from django.db.models.functions import datetime

from hello_django import settings
from .managers import UserManager


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name = "email_address", max_length = 300, unique = True)
    name = models.CharField(max_length = 200)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    spouse_name = models.CharField(blank = True, max_length = 100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email




class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete = models.CASCADE, default = True)
    profile_pic = models.ImageField(default = 'None', upload_to = 'profile_pics', blank = True, null = True)
    bio = models.CharField(default = None, max_length = 500, null = True)
    headline = models.CharField(default = None, max_length = 100, null = True)
    country_code = models.CharField(max_length = 100, null = True, blank = True)
    date_of_birth = models.DateField(verbose_name = 'date_of_birth', blank = True, default = None, null = True)

    def __str__(self):
        return f'{self.user.email}'


class Education(BaseModel):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    highest_education = models.CharField(max_length = 100, default = False)
    highest_education_academy = models.CharField(max_length = 100, default = False)

    def __str__(self):
        return f'{self.user.email}'


class Experience(BaseModel):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    experience = models.CharField(blank = True, max_length = 100, default = False)
    current_designation = models.CharField(max_length = 100, default = False)

    def __str__(self):
        return f'{self.user.email}'


class Feed(BaseModel):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    feed = models.TextField(default = False)

    def __str__(self):
        return f'{self.user.email}'


class Skills(BaseModel):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    skills = models.TextField(blank = True, default = False)

    def __str__(self):
        return f'{self.user.email}'
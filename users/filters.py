from django_filters import rest_framework as filters
from .models import *


class ProfileFilter(filters.FilterSet):
    class Meta:
        model = Profile
        fields = ['bio', 'city']

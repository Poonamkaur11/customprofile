from datetime import timezone

import django_filters
from django.core.mail import send_mail
from django.http import HttpResponse, request
from django_filters import DateFilter, DateRangeFilter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from hello_django import settings
import rest_framework.mixins as mixin
from url_filter.integrations.drf import DjangoFilterBackend


class BaseViewSet(viewsets.ModelViewSet):
    model_class = None
    serializer_class = None
    head = None

    def get_object(self, pk=None):
        queryset = self.get_queryset()
        obj = queryset.get(pk = self.kwargs['pk'])
        return obj

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many = True)
            return self.get_paginated_response({
                "status": "true",
                "message": "data listed successfully.",
                "data": serializer.data
            }
            )

        serializer = self.get_serializer(queryset, many = True)
        return Response({"status": "true", "message": "data listed successfully.", "data": serializer.data})

    def create(self, request, pk=None, *args, **kwargs):

        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                data = {
                    "status": True,
                    "message": f"{self.head} created successfully",
                    "data": serializer.data
                })
        return Response(data = {
            "status": False,
            "message": f"{self.head} created failed",
            "data": serializer.errors
        },
            status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(data = {
            "status": True,
            "message": f"{self.head} data retrieved successfully",
            "data": serializer.data
        }
        )



    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data = request.data, partial = True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                data = {
                    "status": True,
                    "message": f"{self.head} data updated successfully",
                    "data": serializer.data
                })
        return Response(data = {
            "status": False,
            "message": f"{self.head} update failed",
            "data": serializer.errors
        },
            status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(data = {
            "status": True,
            "message": f"{self.head} deleted successfully",
            "data": {}
        },
            status = status.HTTP_200_OK)

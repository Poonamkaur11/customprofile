from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView

from hello_django import settings


class BaseDetails(APIView):
    model_class = None
    serializer_class = None
    head = None

    def get_object(self, pk):
        try:
            return self.model_class.objects.get(pk = pk)
        except self.model_class.DoesNotExist:
            raise ValidationError({
                'status': False,
                'message': f"failed to find {self.head}",
                "data": {}
            })

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj)
        return Response(
            data = {
                "status": True,
                "message": f"{self.head} data retrieved successfully",
                "data": serializer.data
            })

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data = {
                    "status": True,
                    "message": f"{self.head} updated successfully",
                    "data": serializer.data
                })
        return Response(data = {
            "status": False,
            "message": f"{self.head} update failed",
            "data": serializer.errors
        },
            status = status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj,
                                           data = request.data,
                                           partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data = {
                    "status": True,
                    "message": f"{self.head} updated successfully",
                    "data": serializer.data
                })
        return Response(data = {
            "status": False,
            "message": f"{self.head} update failed",
            "data": serializer.errors
        },
            status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(data = {
            "status": True,
            "message": f"{self.head} deleted successfully",
            "data": {}
        },
            status = status.HTTP_200_OK)



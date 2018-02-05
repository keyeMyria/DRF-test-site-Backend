from django.shortcuts import render
from rest_framework.views import APIView
from . import models
from . import serializers
from rest_framework.response import Response


class TagList(APIView):
    def get(self, request):
        queryset = models.Tag.objects.all()
        serializer = serializers.TagListSerializer(queryset, many=True)
        return Response(serializer.data)

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from room.serializers import RoomSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from room.models import Room
from django.core.exceptions import FieldError
from rest_framework import status


def index_page(request):
    return render(request, 'index.html')


class RoomListView(APIView):
    def get(self, request, page, order_field):
        try:
            room_queryset = Room.objects.order_by(order_field)
        except FieldError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if 0 > int(page) > 2:
            return Response(status=status.HTTP_403_FORBIDDEN)
        paginator = Paginator(room_queryset, 12)
        try:
            queryset = paginator.page(page)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

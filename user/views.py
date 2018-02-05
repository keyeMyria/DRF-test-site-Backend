from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, UserSettingsSerializer
from rest_framework import status
from itertools import chain
from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from article.models import Article
from comment.models import ArticleComment
from room.models import Room
from misc.serializers import CurrentActivitySerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class UserInfoPaginationMixIn(object):
    def paginate_response(self, queryset, page):
        paginator = Paginator(queryset, 12)
        try:
            queryset = paginator.page(page)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            queryset = paginator.page(1)

        serializer = CurrentActivitySerializer(queryset, many=True)
        return Response({'data': serializer.data, 'total_pages': paginator.num_pages}, status=status.HTTP_200_OK)


class UserInfoAPI(APIView):
    def get(self, request, username):
        if username == request.user.username:
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                CustomUser.objects.get(username=username)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)


class UserActivity(UserInfoPaginationMixIn, APIView):
    def get(self, request, username, page):
        try:
            user = CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        articles = Article.objects.get(user=user)
        comments = ArticleComment.objects.get(user=user)
        rooms = Room.objects.get(user=user)
        query = sorted(list(chain(articles, comments, rooms)), key=lambda x: x.created, reverse=True)
        return self.paginate_response(query, page)


class UserSettingsAPI(APIView):
    def get(self, request):
        if request.user.is_authenticated():
            serializer = UserSettingsSerializer(request.user.usersettings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        if request.user.is_authenticated():
            data = request.data
            settings = request.user.usersettings
            setattr(settings, data['filter'], data['result'])
            settings.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

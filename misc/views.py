from rest_framework.views import APIView
from article.models import Article
from comment.models import ArticleComment
from room.models import Room
from itertools import chain
from .serializers import CurrentActivitySerializer
from rest_framework.response import Response
from rest_framework import status


class MainPageCurrentActivity(APIView):
    def get(self, request):
        articles = Article.objects.all()[:8]
        comments = ArticleComment.objects.all()[:8]
        rooms = Room.objects.all()[:8]
        query = sorted(list(chain(articles, comments, rooms)), key=lambda x: x.created, reverse=True)[:8]
        serializer = CurrentActivitySerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

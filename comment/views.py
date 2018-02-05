from rest_framework.views import APIView
from article.models import Article
from rest_framework.response import Response
from .serializers import (ArticleCommentSerializer, ArticleCommentSidebar)
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from .models import ArticleComment
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from game_searcher.custom_permissions import AuthorPermission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ArticleListPaginatorMixIn(APIView):
    def paginate_response(self, queryset, page, user):
        paginator = Paginator(queryset, 12)
        try:
            queryset = paginator.page(page)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            queryset = paginator.page(1)

        serializer = ArticleCommentSerializer(queryset, many=True, context={'user': self.request.user})
        return Response({'data': serializer.data, 'total_pages': paginator.num_pages}, status=status.HTTP_200_OK)


class ArticleCommentGlobalRecentComments(APIView):
    def get(self, request, format=None):
        queryset = ArticleComment.objects.all().order_by('-created')[:5]
        serializer = ArticleCommentSidebar(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleCommentList(ArticleListPaginatorMixIn, APIView):

    def _get_object(self, pk):
        try:
            return Article.objects.get(primary_key=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, page):
        article = self._get_object(pk)
        queryset = article.articlecomment_set.order_by('created')
        return self.paginate_response(queryset, page, request.user)


class ArticleCommentAPI(APIView):
    authentication_classes = (IsAuthenticated, AuthorPermission,)

    def patch(self, request, pk, format=None):
        try:
            comment = ArticleComment.objects.get(pk=pk)
            serializer = ArticleCommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({"popup_message": "comment doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            comment = ArticleComment.objects.get(pk=pk)
            comment.delete()
            return Response({'popup_message': 'message has been deleted'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"popup_message": "comment doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

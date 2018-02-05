from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from . import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from hit_count.models import Hit
from utils.utl import get_ip
from .models import Subscription
from tag.models import Tag
from django.db.models import Q


class ArticleListPaginatorMixIn(APIView):
    def paginate_response(self, queryset, page):
        paginator = Paginator(queryset, 12)
        try:
            queryset = paginator.page(page)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            queryset = paginator.page(1)

        serializer = serializers.ArticleSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'total_pages': paginator.num_pages}, status=status.HTTP_200_OK)


class ArticleListPreview(APIView):
    def get(self, request, page):
        if 0 > int(page) > 2:
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset = models.Article.objects.all().order_by('-created')[:12]
        paginator = Paginator(queryset, 6)
        try:
            queryset = paginator.page(page)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        serializer = serializers.ArticleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleListMixIn(object):
    def get_article_list(self, order, tag, search):
        if search:
            return models.Article.objects.filter(Q(title__contains=search) | Q(text__contains=search))
        elif tag:
            return Tag.get_article_by_tag(tag)
        elif order:
            return models.Article.objects.all().order_by(order)
        return models.Article.objects.all().order_by('-created')


class ArticleListView(ArticleListPaginatorMixIn, ArticleListMixIn, APIView):

    def get(self, request, page, order, tag=None, search=None, format=None):
        queryset = self.get_article_list(order, tag, search)
        return self.paginate_response(queryset, page)


class ArticleDetailsView(APIView):

    def _add_hit(self, hit_counter):
        Hit.objects.get_or_create(session=self.request.session.session_key,
                                  hitcount=hit_counter,
                                  ip=get_ip(self.request))

    def get(self, request, pk, format=None):
        try:
            article = models.Article.objects.get(pk=pk)
            self._add_hit(article.hitcount)
            serializer = serializers.ArticleSerializer(article)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Subscribe(APIView):
    def get(self, request, pk):
        if request.user.is_authenticated() is False:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            subscription = Subscription.objects.get(article_id=pk, user=request.user)
            subscription.delete()
        except ObjectDoesNotExist:
            Subscription.objects.create(article_id=pk, user=request.user)
        return Response(status=status.HTTP_200_OK)

from rest_framework import serializers
from . import models
from django.utils import formats
from hit_count import models
from tag.models import Tag


class HitSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HitCount
        fields = ('hits',)


class ArticleSerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    hitcount = serializers.SerializerMethodField()
    tag_list = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    like_counter = serializers.SerializerMethodField()

    class Meta:
        model = models.Article
        fields = ('created', 'title', 'theme', 'text', 'image',
                  'primary_key', 'user', 'pretext', 'hitcount',
                  'like_counter', 'tag_list',
                  'total_subscriptions', 'total_comments')

    def get_tag_list(self, obj):
        return obj.tag_set.all().values_list('text', flat=True)

    def get_like_counter(self, obj):
        like_counter = obj.likecounter
        return {'likes': like_counter.likes, 'dislikes': like_counter.dislikes}

    def get_created(self, obj):
        return formats.date_format(obj.created, "d M h:i")

    def get_image(self, obj):
        return obj.get_image()

    def get_user(self, obj):
        return obj.user.username

    def get_hitcount(self, obj):
        return obj.hitcount.hits

    def get_total_comments(self, obj):
        return obj.articlecomment_set.count()


class ArticleListSidebar(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = models.Article
        fields = ('title', 'created', 'total_likes', 'total_comments')

    def get_total_likes(self, obj):
        return obj.likecounter.likes

    def get_created(self, obj):
        return formats.date_format(obj.created, 'd/m/y')


class ArticleListSidebarHits(serializers.ModelSerializer):
    total_hits = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = models.Article
        fields = ('title', 'created', 'total_hits', 'total_comments')

    def get_total_hits(self, obj):
        return obj.hitcount.hits

    def get_created(self, obj):
        return formats.date_format(obj.created, 'd/m/y')

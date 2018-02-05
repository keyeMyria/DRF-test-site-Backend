from rest_framework import serializers
from . import models
from django.utils import formats
from .models import ArticleComment


class RecursiveField(serializers.ModelSerializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ArticleCommentSerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    likecounter = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    child_comments_set = RecursiveField(many=True, required=False, context={})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context.get('user')

    class Meta:
        model = models.ArticleComment
        fields = ('id', 'created', 'text', 'user', 'username', 'child_comments_set', 'parent', 'likecounter', 'liked')

    def get_created(self, obj):
        return formats.date_format(obj.created, "d M h:i")

    def get_username(self, obj):
        return obj.user.username

    def get_liked(self, obj):
        likes = obj.likecounter.like_set.filter(user=self.user)
        if len(likes) == 0:
            return None
        else:
            return True if likes[0].like_status is True else False

    def get_likecounter(self, obj):
        return {'likes': obj.likecounter.likes, 'dislikes': obj.likecounter.dislikes}

    def validate_text(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('a comment must contain at least 5 symbols')
        return value

    def get_child_comments_set(self, obj):
        return obj.child_comments_set.all().order_by('created')

    def create(self, validated_data):
        return models.ArticleComment.objects.create(**validated_data)


class ArticleCommentSidebar(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    article_title = serializers.SerializerMethodField()
    article_pk = serializers.SerializerMethodField()

    class Meta:
        model = ArticleComment
        fields = ('created', 'text', 'username', 'article_title', 'article_pk')

    def get_username(self, obj):
        return obj.user.username

    def get_created(self, obj):
        return formats.date_format(obj.created, 'd/m/y')

    def get_article_title(self, obj):
        return obj.article.title

    def get_article_pk(self, obj):
        return obj.article.primary_key

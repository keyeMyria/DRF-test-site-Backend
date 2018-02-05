from rest_framework import serializers
from . import models


class LikeSerializer(serializers.ModelSerializer):
    comment_pk = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    like_counter = serializers.SerializerMethodField()

    class Meta:
        model = models.Like
        fields = ('user', 'like_counter', 'comment_pk', 'like_status')

    def get_comment_pk(self, obj):
        return obj.like_counter.comment.pk

    def get_user(self, obj):
        return obj.user.username

    def validate_user(self, value):
        if value is None:
            raise serializers.ValidationError('only authorised users can like')
        return value

    def get_like_counter(self, obj):
        return {'likes': obj.like_counter.likes, 'dislikes': obj.like_counter.dislikes}

    def validate_like_counter(self, value):
        if value is None:
            raise serializers.ValidationError("comment doesn't exist")
        return value

    def create(self, validated_data):
        return models.Like.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.like_status = validated_data['like_status']
        instance.save()
        return instance

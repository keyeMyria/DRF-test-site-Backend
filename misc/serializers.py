from rest_framework import serializers
from django.utils import formats


class CurrentActivitySerializer(serializers.Serializer):
    created = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_created(self, obj):
        return formats.date_format(obj.created, 'd/m/y')

    def get_text(self, obj):
        return obj.get_activity_text()

    def get_username(self, obj):
        return obj.user.username

    def get_name(self, obj):
        try:
            return obj.title
        except AttributeError:
            try:
                return obj.article.title
            except AttributeError:
                return obj.name

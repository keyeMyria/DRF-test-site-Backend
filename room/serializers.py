from rest_framework import serializers
from room.models import Room
from django.utils import formats


class RoomSerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    current_users = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('created', 'size', 'name', 'locked', 'username', 'current_users')

    def get_username(self, obj):
        return obj.user.username

    def get_current_users(self, obj):
        return obj.current_users()

    def get_created(self, obj):
        return formats.date_format(obj.created, 'd/m/y')

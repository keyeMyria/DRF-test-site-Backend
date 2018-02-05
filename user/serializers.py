from rest_framework import serializers
from .models import CustomUser, UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        exclude = ('user', )


class UserSerializer(serializers.ModelSerializer):
    rating_stats = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('username', 'rating_stats')

    def get_rating_stats(self, obj):
        like_counter = obj.userlikecounter
        return {'likes': like_counter.likes, 'dislikes': like_counter.dislikes}

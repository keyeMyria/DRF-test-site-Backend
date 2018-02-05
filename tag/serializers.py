from rest_framework.serializers import ModelSerializer
from . import models


class TagListSerializer(ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('text', )

from django.db import models
from django.utils import timezone
from article.models import Article
from django.conf import settings


class Tag(models.Model):
    text = models.CharField(max_length=25)
    created = models.DateTimeField(default=timezone.now)
    article = models.ManyToManyField(Article)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)

    @staticmethod
    def get_article_by_tag(text):
        return Tag.objects.get(text=text).article.all()

    def __str__(self):
        return self.text

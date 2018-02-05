from django.db import models
from article.models import Article
from comment.models import ArticleComment
from django.conf import settings
from django.utils import timezone


class LikeModelMeta(models.Model):
    created = models.DateTimeField(default=timezone.now)
    likes = models.SmallIntegerField(default=0)
    dislikes = models.SmallIntegerField(default=0)

    class Meta:
        abstract = True


class UserLikeCounter(LikeModelMeta):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class LikeCounter(LikeModelMeta):
    article = models.OneToOneField(Article, blank=True, null=True, on_delete=models.CASCADE)
    comment = models.OneToOneField(ArticleComment, blank=True, null=True, on_delete=models.CASCADE)

    def get_like_objects(self):
        return self.like_set.filter(like=True)

    def get_dislike_objects(self):
        return self.like_set.filter(like=False)

    def __str__(self):
        if self.article:
            str_object = self.article
        else:
            str_object = self.comment
        return 'like counter of {0}'.format(str_object)

    def save(self, *args, **kwargs):
        if self.article and self.comment:
            raise ValueError
        super().save(*args, **kwargs)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_counter = models.ForeignKey(LikeCounter, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    like_status = models.BooleanField(default=True)

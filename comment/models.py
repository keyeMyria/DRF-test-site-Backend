from django.db import models
from article.models import Article
from django.utils import timezone
from django.conf import settings


class ArticleComment(models.Model):
    created = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child_comments_set', on_delete=models.CASCADE)
    answer_target = models.ForeignKey('self', null=True, blank=True, related_name='target_comment', on_delete=models.CASCADE)

    def get_activity_text(self):
        return ' оставил комментарий в теме '

    def get_class_name(self):
        return self.__class__.__name__.lower()

    def __str__(self):
        return '{0}'.format(self.id)

    def save(self, *args, **kwargs):
        if self.answer_target:
            if self.answer_target.parent:
                self.parent = self.answer_target.parent
            else:
                self.parent = self.answer_target
        super().save(*args, **kwargs)

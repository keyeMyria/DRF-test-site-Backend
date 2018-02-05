from article.models import Article
from comment.models import ArticleComment
from django.db.models.signals import (post_save, pre_save, post_delete)
from django.dispatch import receiver
from .models import (Like, LikeCounter)
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=Like)
@receiver(post_delete, sender=Like)
def like_model_save(sender, instance, **kwargs):
    like_counter = instance.like_counter
    like_counter.likes = like_counter.like_set.filter(like_status=True).count()
    like_counter.dislikes = like_counter.like_set.filter(like_status=False).count()
    return like_counter.save()


@receiver(post_save, sender=Article)
@receiver(post_save, sender=ArticleComment)
def like_counter_save(sender, instance, **kwargs):
    if instance.get_class_name() == 'article':
        return LikeCounter.objects.get_or_create(article=instance)
    else:
        return LikeCounter.objects.get_or_create(comment=instance)

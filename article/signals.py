from django.db.models.signals import (post_save, pre_save, pre_delete)
from django.dispatch import receiver
from comment.models import ArticleComment
from django.core.exceptions import ObjectDoesNotExist
from .models import Subscription


@receiver(pre_save, sender=ArticleComment)
def comment_save(sender, instance, **kwargs):
    try:
        ArticleComment.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        instance.article.total_comments += 1
        return instance.article.save()


@receiver(pre_delete, sender=ArticleComment)
def comment_delete(sender, instance, **kwargs):
    instance.article.total_comments -= 1
    return instance.article.save()


@receiver(pre_save, sender=Subscription)
def subscription_save(sender, instance, **kwargs):
    instance.article.total_subscriptions += 1
    return instance.article.save()


@receiver(pre_delete, sender=Subscription)
def subscription_delete(sender, instance, **kwargs):
    instance.article.total_subscriptions -= 1
    return instance.article.save()
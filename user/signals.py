from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models
from django.core.exceptions import ObjectDoesNotExist
from like.models import UserLikeCounter


@receiver(post_save, sender=models.CustomUser)
def user_settings(sender, instance, **kwargs):
    try:
        models.UserSettings.objects.get(user=instance)
    except ObjectDoesNotExist:
        models.UserSettings.objects.create(user=instance)
    try:
        UserLikeCounter.objects.get(user=instance)
    except ObjectDoesNotExist:
        UserLikeCounter.objects.create(user=instance)


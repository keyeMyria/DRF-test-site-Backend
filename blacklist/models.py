from django.db import models
from django.conf import settings
from django.utils import timezone


class BlackList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Blacklist of {0}'.format(self.user.username)


class BlackListedUser(models.Model):
    blacklist = models.ForeignKey(BlackList, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}'.format(self.user.username)

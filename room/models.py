from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Room(models.Model):
    created = models.DateTimeField(default=timezone.now)
    size = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(64)])
    name = models.CharField(max_length=50)
    locked = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def current_users(self):
        return self.signedupuser_set.all().count()

    def get_activity_text(self):
        return ' создал комнату '


class SignedUpUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    join_date = models.DateTimeField(default=timezone.now)

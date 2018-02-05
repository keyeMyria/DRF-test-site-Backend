from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings


class ArticleImage(models.Model):
    image = models.ImageField()
    created = models.DateTimeField(default=timezone.now)


class Article(models.Model):
    THEME_CHOICES = (
      ('EU4', 'Europa Universalis IV'),
      ('HOI4', 'Hearts of Iron 4'),
      ('OFF', 'Other')
    )

    created = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=50)
    text = models.TextField()
    theme = models.CharField(choices=THEME_CHOICES, max_length=50)
    primary_key = models.SlugField(primary_key=True, unique=True, max_length=100, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pretext = models.TextField(blank=True, null=True)

    total_comments = models.SmallIntegerField(default=0)
    total_subscriptions = models.SmallIntegerField(default=0)

    def __str__(self):
        return '{0} {1}'.format(self.get_class_name(), self.title)

    def get_activity_text(self):
        return ' создал тему '

    def get_image(self):
        try:
            return self.image.image.url
        except AttributeError:
            return

    def get_class_name(self):
        return self.__class__.__name__.lower()

    def save(self, *args, **kwargs):
        if not self.primary_key:
            self.primary_key = slugify(self.title)
        super().save(*args, **kwargs)


class Subscription(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    new_comments = models.SmallIntegerField(default=0)

    def __str__(self):
        return 'sub of {0} on {1}'.format(self.user, self.article)

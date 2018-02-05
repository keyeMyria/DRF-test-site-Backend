from django.contrib import admin
from . import models


admin.site.register(models.Article)
admin.site.register(models.ArticleImage)
admin.site.register(models.Subscription)

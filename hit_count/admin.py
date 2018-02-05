from django.contrib import admin
from . import models


admin.site.register(models.Hit)
admin.site.register(models.HitCount)

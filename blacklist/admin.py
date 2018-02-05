from django.contrib import admin
from . import models


admin.site.register(models.BlackList)
admin.site.register(models.BlackListedUser)

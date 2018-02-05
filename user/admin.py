from django.contrib import admin
from .models import CustomUser, UserSettings


admin.site.register(CustomUser)
admin.site.register(UserSettings)

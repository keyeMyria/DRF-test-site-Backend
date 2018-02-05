from django.contrib import admin
from .models import Like, LikeCounter


admin.site.register(LikeCounter)
admin.site.register(Like)

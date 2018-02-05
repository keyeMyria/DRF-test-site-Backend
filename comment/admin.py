from django.contrib import admin
from .models import ArticleComment


class ArticleCommentExtension(admin.ModelAdmin):
    list_display = ('id', 'created', 'text', 'user', 'answer_target', 'parent')


admin.site.register(ArticleComment, ArticleCommentExtension)

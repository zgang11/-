# Register your models here.
from django.contrib import admin

from .models import ArticlePost, DailyData

admin.site.register(ArticlePost)
admin.site.register(DailyData)


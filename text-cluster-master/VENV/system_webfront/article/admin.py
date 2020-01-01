# Register your models here.
from django.contrib import admin

from .models import ArticlePost, DailyData, DailyData_Tags

admin.site.register(ArticlePost)
admin.site.register(DailyData)
admin.site.register(DailyData_Tags)

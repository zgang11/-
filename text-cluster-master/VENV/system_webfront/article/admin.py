from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Column, Article

admin.site.register(Column, Article)
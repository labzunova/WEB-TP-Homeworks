from django.contrib import admin
from app import models

admin.site.register(models.Article)
admin.site.register(models.Author)

# Register your models here.

from django.contrib import admin


# Register your models here.
from meiduo.apps.contents import models

admin.site.register(models.Content)
admin.site.register(models.ContentCategory)
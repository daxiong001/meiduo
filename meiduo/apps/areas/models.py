from django.db import models

# Create your models here.
from meiduo.utils.models import BaseModel


class Area(models.Model):
    """省市区"""
    name = models.CharField(max_length=20, verbose_name="名称")
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, related_name='subs', blank=True, null=True)

    class Meta:
        db_table = "tb_areas"
        verbose_name = "行政区域"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



from django.db import models
from django.contrib.auth.models import AbstractUser
from meiduo.apps.areas.models import Area

# Create your models here.
from meiduo.utils.models import BaseModel


class User(AbstractUser):
    """自定义用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    email_active = models.BooleanField(default=False, verbose_name="邮箱")
    default_address = models.ForeignKey("Address", related_name="users", on_delete=models.SET_NULL, null=True,
                                        blank=True, verbose_name="默认地址")

    class Meta:
        db_table = 'tb_user'
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Address(BaseModel):
    """收货地址"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="address", verbose_name="用户")
    title = models.CharField(max_length=20, verbose_name="地址名称")
    receiver = models.CharField(max_length=20, verbose_name="收货人")
    province = models.ForeignKey(Area, on_delete=models.PROTECT, related_name="province_addresses", verbose_name="省")
    city = models.ForeignKey(Area, on_delete=models.PROTECT, related_name="city_addresses", verbose_name="市")
    district = models.ForeignKey(Area, on_delete=models.PROTECT, related_name="district_addresses", verbose_name="区")
    place = models.CharField(max_length=50, verbose_name="地址")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    tel = models.CharField(max_length=20, verbose_name="固定电话", null=True, blank=True, default="")
    email = models.CharField(max_length=30, null=True, blank=True, verbose_name="邮箱")
    is_deleted = models.BooleanField(default=False, verbose_name="逻辑删除")

    class Meta:
        db_table = "tb_address"
        verbose_name = "用户地址"
        verbose_name_plural = verbose_name
        ordering = ["-update_time"]

    def __str__(self):
        return self.province.name, self.city.name, self.district.name, self.place

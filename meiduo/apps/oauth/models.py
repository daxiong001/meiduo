from django.db import models


# Create your models here.
from meiduo.apps.users.models import User
from meiduo.utils.models import BaseModel


class OAuthWeiBoUser(BaseModel):
    """
    微博用户登陆数据
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    openid = models.CharField(max_length=64, verbose_name="openid", db_index=True)

    class Meta:
        db_table = 'tb_oauth_wb'
        verbose_name = "微博登陆用户数据"
        verbose_name_plural = verbose_name